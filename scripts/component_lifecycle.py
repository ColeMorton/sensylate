#!/usr/bin/env python3
"""
Component Lifecycle Interface

Defines standard lifecycle phases for pipeline components:
- init(): Basic initialization, no expensive operations
- configure(): Configuration and cache setup, expensive operations allowed
- start(): Begin active operations, use cached configuration

This interface enables proper dependency ordering, lazy initialization,
and configuration caching to eliminate redundant expensive operations.
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class ComponentState(Enum):
    """Component lifecycle states"""
    UNINITIALIZED = "uninitialized"
    INITIALIZED = "initialized" 
    CONFIGURED = "configured"
    STARTED = "started"
    STOPPED = "stopped"
    FAILED = "failed"


class ComponentLifecycle(ABC):
    """
    Abstract base class for pipeline components with standardized lifecycle management
    
    Lifecycle phases:
    1. init() - Basic initialization, dependency injection, no expensive operations
    2. configure() - Configuration setup, cache initialization, expensive discovery operations
    3. start() - Begin active operations using cached configuration
    4. stop() - Cleanup and shutdown (optional)
    """

    def __init__(self, component_name: str):
        self.component_name = component_name
        self.state = ComponentState.UNINITIALIZED
        self.logger = logging.getLogger(f"component.{component_name}")
        self.initialization_time: Optional[datetime] = None
        self.configuration_time: Optional[datetime] = None
        self.start_time: Optional[datetime] = None
        
        # Cache for expensive operations performed in configure() phase
        self._configuration_cache: Dict[str, Any] = {}
        self._cache_valid = False
        
    def get_state(self) -> ComponentState:
        """Get current component state"""
        return self.state
        
    def is_configured(self) -> bool:
        """Check if component is properly configured"""
        return self.state in [ComponentState.CONFIGURED, ComponentState.STARTED]
        
    def is_started(self) -> bool:
        """Check if component is started and ready for operations"""
        return self.state == ComponentState.STARTED
        
    def get_cache(self, key: str) -> Optional[Any]:
        """Get cached configuration data"""
        if not self._cache_valid:
            return None
        return self._configuration_cache.get(key)
        
    def set_cache(self, key: str, value: Any) -> None:
        """Set cached configuration data"""
        self._configuration_cache[key] = value
        self._cache_valid = True
        
    def invalidate_cache(self) -> None:
        """Invalidate configuration cache (forces reconfigure on next operation)"""
        self._configuration_cache.clear()
        self._cache_valid = False
        self.logger.debug(f"Configuration cache invalidated for {self.component_name}")
        
    def init(self) -> None:
        """
        Phase 1: Basic initialization
        - Set up basic component state
        - Initialize dependencies (but don't use them yet)
        - No expensive operations allowed
        """
        if self.state != ComponentState.UNINITIALIZED:
            raise RuntimeError(f"Component {self.component_name} already initialized (state: {self.state})")
            
        try:
            self.initialization_time = datetime.now()
            self._do_init()
            self.state = ComponentState.INITIALIZED
            self.logger.debug(f"Component {self.component_name} initialized successfully")
            
        except Exception as e:
            self.state = ComponentState.FAILED
            self.logger.error(f"Component {self.component_name} initialization failed: {e}")
            raise
            
    def configure(self, force_reconfigure: bool = False) -> None:
        """
        Phase 2: Configuration and cache setup
        - Perform expensive discovery and setup operations
        - Cache results for reuse in start() phase
        - Only run once unless forced or cache invalidated
        """
        if self.state == ComponentState.UNINITIALIZED:
            raise RuntimeError(f"Component {self.component_name} must be initialized before configuration")
            
        if self.state == ComponentState.FAILED:
            raise RuntimeError(f"Component {self.component_name} is in failed state and cannot be configured")
            
        # Skip configuration if already configured and cache is valid
        if self.is_configured() and self._cache_valid and not force_reconfigure:
            self.logger.debug(f"Component {self.component_name} already configured, using cached configuration")
            return
            
        try:
            self.configuration_time = datetime.now()
            self.logger.debug(f"Configuring component {self.component_name}...")
            
            # Invalidate cache before reconfiguration
            self.invalidate_cache()
            
            self._do_configure()
            self.state = ComponentState.CONFIGURED
            self.logger.debug(f"Component {self.component_name} configured successfully")
            
        except Exception as e:
            self.state = ComponentState.FAILED
            self.logger.error(f"Component {self.component_name} configuration failed: {e}")
            raise
            
    def start(self) -> None:
        """
        Phase 3: Begin active operations
        - Use cached configuration from configure() phase
        - Perform actual work operations
        - Can be called multiple times after configuration
        """
        if not self.is_configured():
            raise RuntimeError(f"Component {self.component_name} must be configured before starting")
            
        if self.state == ComponentState.FAILED:
            raise RuntimeError(f"Component {self.component_name} is in failed state and cannot be started")
            
        try:
            self.start_time = datetime.now()
            self._do_start()
            self.state = ComponentState.STARTED
            self.logger.debug(f"Component {self.component_name} started successfully")
            
        except Exception as e:
            self.state = ComponentState.FAILED
            self.logger.error(f"Component {self.component_name} start failed: {e}")
            raise
            
    def stop(self) -> None:
        """
        Phase 4: Cleanup and shutdown (optional)
        - Clean up resources
        - Stop active operations
        - Preserve configuration cache for restart
        """
        if self.state not in [ComponentState.STARTED, ComponentState.CONFIGURED]:
            self.logger.warning(f"Component {self.component_name} not running (state: {self.state})")
            return
            
        try:
            self._do_stop()
            self.state = ComponentState.STOPPED
            self.logger.debug(f"Component {self.component_name} stopped successfully")
            
        except Exception as e:
            self.state = ComponentState.FAILED
            self.logger.error(f"Component {self.component_name} stop failed: {e}")
            raise
    
    def get_lifecycle_info(self) -> Dict[str, Any]:
        """Get component lifecycle information for debugging/monitoring"""
        return {
            "component_name": self.component_name,
            "state": self.state.value,
            "initialization_time": self.initialization_time.isoformat() if self.initialization_time else None,
            "configuration_time": self.configuration_time.isoformat() if self.configuration_time else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "cache_valid": self._cache_valid,
            "cache_keys": list(self._configuration_cache.keys()),
        }
        
    # Abstract methods that concrete components must implement
    
    @abstractmethod
    def _do_init(self) -> None:
        """Perform component-specific initialization"""
        pass
        
    @abstractmethod
    def _do_configure(self) -> None:
        """Perform component-specific configuration and caching"""
        pass
        
    @abstractmethod
    def _do_start(self) -> None:
        """Perform component-specific start operations"""
        pass
        
    def _do_stop(self) -> None:
        """Perform component-specific stop operations (optional override)"""
        pass


class ComponentLifecycleManager:
    """
    Manages the lifecycle of multiple components with proper dependency ordering
    """
    
    def __init__(self):
        self.components: Dict[str, ComponentLifecycle] = {}
        self.dependency_order: list[str] = []
        self.logger = logging.getLogger("component.lifecycle_manager")
        
    def register_component(self, component: ComponentLifecycle, dependencies: list[str] = None) -> None:
        """
        Register a component with optional dependencies
        
        Args:
            component: Component to register
            dependencies: List of component names this component depends on
        """
        if dependencies is None:
            dependencies = []
            
        self.components[component.component_name] = component
        
        # Simple dependency ordering (topological sort would be better for complex dependencies)
        for dep in dependencies:
            if dep not in self.dependency_order:
                self.dependency_order.append(dep)
                
        if component.component_name not in self.dependency_order:
            self.dependency_order.append(component.component_name)
            
        self.logger.debug(f"Registered component {component.component_name} with dependencies: {dependencies}")
        
    def initialize_all(self) -> None:
        """Initialize all components in dependency order"""
        for component_name in self.dependency_order:
            if component_name in self.components:
                self.logger.debug(f"Initializing component: {component_name}")
                self.components[component_name].init()
                
    def configure_all(self, force_reconfigure: bool = False) -> None:
        """Configure all components in dependency order"""
        for component_name in self.dependency_order:
            if component_name in self.components:
                self.logger.debug(f"Configuring component: {component_name}")
                self.components[component_name].configure(force_reconfigure)
                
    def start_all(self) -> None:
        """Start all components in dependency order"""
        for component_name in self.dependency_order:
            if component_name in self.components:
                self.logger.debug(f"Starting component: {component_name}")
                self.components[component_name].start()
                
    def stop_all(self) -> None:
        """Stop all components in reverse dependency order"""
        for component_name in reversed(self.dependency_order):
            if component_name in self.components:
                self.logger.debug(f"Stopping component: {component_name}")
                self.components[component_name].stop()
                
    def get_component(self, component_name: str) -> Optional[ComponentLifecycle]:
        """Get a registered component by name"""
        return self.components.get(component_name)
        
    def get_all_lifecycle_info(self) -> Dict[str, Dict[str, Any]]:
        """Get lifecycle information for all components"""
        return {
            name: component.get_lifecycle_info() 
            for name, component in self.components.items()
        }