#!/usr/bin/env python3
"""
Preference Learning Engine
Adapts suggestion algorithms based on user choices, success rates, and feedback patterns
"""

import json
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import statistics

@dataclass
class UserInteractionPattern:
    """Represents a pattern in user interactions"""
    command: str
    context_features: Dict[str, Any]
    user_action: str  # executed, rejected, deferred
    success_rate: float
    frequency: int
    confidence_threshold: float
    time_preference: int  # seconds
    last_updated: datetime

@dataclass
class LearningModel:
    """Machine learning model for preference prediction"""
    feature_weights: Dict[str, float]
    confidence_adjustments: Dict[str, float]
    temporal_patterns: Dict[str, List[int]]  # hour -> preference scores
    success_predictors: Dict[str, float]
    model_accuracy: float
    training_samples: int
    last_trained: datetime

class PreferenceLearningEngine:
    """Intelligent learning system for user workflow preferences"""

    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path or "team-workspace")
        self.learning_path = self.workspace_path / "framework" / "learning"
        self.learning_path.mkdir(parents=True, exist_ok=True)

        # Learning data storage
        self.patterns_path = self.learning_path / "patterns"
        self.patterns_path.mkdir(exist_ok=True)

        self.models_path = self.learning_path / "models"
        self.models_path.mkdir(exist_ok=True)

        # Initialize learning components
        self.pattern_analyzer = UserPatternAnalyzer(self.workspace_path)
        self.preference_predictor = PreferencePredictor(self.workspace_path)
        self.adaptation_engine = AdaptationEngine(self.workspace_path)

        # Load existing learning models
        self.learning_models = self._load_learning_models()

        # User interaction tracking
        self.interaction_history = defaultdict(list)
        self._load_interaction_history()

    def learn_from_interaction(self, user_id: str, command: str,
                             suggestion_context: Dict[str, Any],
                             user_action: str, outcome: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from user interaction and update preferences"""

        # Extract features from context
        features = self._extract_features(suggestion_context)

        # Record interaction
        interaction = {
            "user_id": user_id,
            "command": command,
            "features": features,
            "action": user_action,
            "outcome": outcome,
            "timestamp": datetime.now().isoformat()
        }

        self.interaction_history[user_id].append(interaction)

        # Analyze patterns
        patterns = self.pattern_analyzer.analyze_user_patterns(user_id, self.interaction_history[user_id])

        # Update learning models
        model_updates = self._update_learning_models(user_id, interaction, patterns)

        # Generate adaptation recommendations
        adaptations = self.adaptation_engine.generate_adaptations(user_id, patterns)

        # Save learning data
        self._save_learning_data(user_id, interaction, patterns, adaptations)

        return {
            "patterns_updated": len(patterns),
            "model_accuracy": model_updates.get("accuracy", 0.0),
            "adaptations_generated": len(adaptations),
            "learning_confidence": self._calculate_learning_confidence(user_id),
            "recommendations": adaptations
        }

    def predict_user_preference(self, user_id: str, command: str,
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Predict user preference for a suggestion"""

        # Extract features
        features = self._extract_features(context)

        # Get user patterns
        user_patterns = self._get_user_patterns(user_id, command)

        # Predict acceptance probability
        acceptance_probability = self.preference_predictor.predict_acceptance(
            user_id, command, features, user_patterns
        )

        # Predict optimal parameters
        optimal_params = self.preference_predictor.predict_optimal_parameters(
            user_id, command, features, user_patterns
        )

        # Calculate confidence adjustments
        confidence_adjustment = self._calculate_confidence_adjustment(
            user_id, command, features
        )

        return {
            "acceptance_probability": acceptance_probability,
            "optimal_parameters": optimal_params,
            "confidence_adjustment": confidence_adjustment,
            "recommendation_strength": self._assess_recommendation_strength(
                acceptance_probability, confidence_adjustment
            ),
            "personalization_factors": self._identify_personalization_factors(
                user_id, command, features
            )
        }

    def _assess_recommendation_strength(self, acceptance_probability: float,
                                      confidence_adjustment: float) -> str:
        """Assess strength of recommendation"""

        combined_score = acceptance_probability + confidence_adjustment

        if combined_score > 0.9:
            return "very_strong"
        elif combined_score > 0.7:
            return "strong"
        elif combined_score > 0.5:
            return "moderate"
        else:
            return "weak"

    def _identify_personalization_factors(self, user_id: str, command: str,
                                        features: Dict[str, Any]) -> List[str]:
        """Identify factors that influenced personalization"""

        factors = []

        # Check learned patterns
        user_patterns = self._get_user_patterns(user_id, command)
        if user_patterns:
            factors.append("historical_patterns")

        # Check temporal factors
        model_key = f"user_{user_id}"
        if model_key in self.learning_models:
            model = self.learning_models[model_key]
            if command in model.temporal_patterns:
                factors.append("temporal_preferences")

            if command in model.confidence_adjustments:
                factors.append("confidence_learning")

        # Check feature learning
        if features:
            factors.append("context_adaptation")

        return factors

    def adapt_suggestion_thresholds(self, user_id: str,
                                  suggestions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Adapt suggestion confidence thresholds based on learned preferences"""

        adapted_suggestions = []

        for suggestion in suggestions:
            command = suggestion.get("command", "")
            original_confidence = suggestion.get("confidence", 0.0)

            # Get learned adjustments
            user_patterns = self._get_user_patterns(user_id, command)
            confidence_adjustment = self._calculate_confidence_adjustment(
                user_id, command, suggestion
            )

            # Apply temporal adjustments
            temporal_adjustment = self._get_temporal_adjustment(user_id, command)

            # Calculate adapted confidence
            adapted_confidence = min(1.0, max(0.0,
                original_confidence + confidence_adjustment + temporal_adjustment
            ))

            # Update suggestion
            adapted_suggestion = suggestion.copy()
            adapted_suggestion["original_confidence"] = original_confidence
            adapted_suggestion["confidence"] = adapted_confidence
            adapted_suggestion["personalization_applied"] = True
            adapted_suggestion["adjustment_factors"] = {
                "user_preference": confidence_adjustment,
                "temporal": temporal_adjustment,
                "total_adjustment": adapted_confidence - original_confidence
            }

            adapted_suggestions.append(adapted_suggestion)

        return adapted_suggestions

    def get_learning_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights into user learning patterns and preferences"""

        user_interactions = self.interaction_history.get(user_id, [])

        if not user_interactions:
            return {"status": "insufficient_data", "interactions": 0}

        # Calculate learning metrics
        learning_metrics = self._calculate_learning_metrics(user_id)

        # Identify strong preferences
        strong_preferences = self._identify_strong_preferences(user_id)

        # Analyze temporal patterns
        temporal_patterns = self._analyze_temporal_patterns(user_id)

        # Calculate prediction accuracy
        prediction_accuracy = self._calculate_prediction_accuracy(user_id)

        return {
            "status": "sufficient_data",
            "interactions": len(user_interactions),
            "learning_metrics": learning_metrics,
            "strong_preferences": strong_preferences,
            "temporal_patterns": temporal_patterns,
            "prediction_accuracy": prediction_accuracy,
            "personalization_effectiveness": self._assess_personalization_effectiveness(user_id),
            "recommendations": self._generate_learning_recommendations(user_id)
        }

    def _extract_features(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant features from suggestion context"""

        features = {}

        # Temporal features
        now = datetime.now()
        features["hour"] = now.hour
        features["day_of_week"] = now.weekday()
        features["is_weekend"] = now.weekday() >= 5

        # Context features
        features["estimated_time"] = context.get("estimated_time", 0)
        features["confidence"] = context.get("confidence", 0.0)
        features["priority"] = context.get("priority", "medium")

        # Task features
        features["command_complexity"] = self._assess_command_complexity(
            context.get("command", "")
        )
        features["has_dependencies"] = bool(context.get("dependencies", []))
        features["output_type"] = context.get("output_type", "text")

        # User context features
        features["current_workflow"] = context.get("current_workflow", "general")
        features["recent_activity"] = context.get("recent_activity", "normal")

        return features

    def _update_learning_models(self, user_id: str, interaction: Dict[str, Any],
                              patterns: List[UserInteractionPattern]) -> Dict[str, Any]:
        """Update learning models based on new interaction"""

        model_key = f"user_{user_id}"

        if model_key not in self.learning_models:
            self.learning_models[model_key] = self._create_new_learning_model()

        model = self.learning_models[model_key]

        # Update feature weights
        self._update_feature_weights(model, interaction)

        # Update confidence adjustments
        self._update_confidence_adjustments(model, interaction)

        # Update temporal patterns
        self._update_temporal_patterns(model, interaction)

        # Update success predictors
        self._update_success_predictors(model, interaction)

        # Retrain model if enough new data
        model.training_samples += 1
        if model.training_samples % 10 == 0:  # Retrain every 10 interactions
            model.model_accuracy = self._retrain_model(user_id, model)
            model.last_trained = datetime.now()

        # Save updated model
        self._save_learning_model(model_key, model)

        return {
            "accuracy": model.model_accuracy,
            "training_samples": model.training_samples,
            "features_updated": len(model.feature_weights)
        }

    def _update_feature_weights(self, model: LearningModel, interaction: Dict[str, Any]):
        """Update feature weights based on interaction"""

        features = interaction["features"]
        action = interaction["action"]

        # Weight update factor based on action
        weight_factor = 0.1 if action == "executed" else -0.05

        for feature, value in features.items():
            if feature not in model.feature_weights:
                model.feature_weights[feature] = 0.0

            # Update weight based on feature value and action
            if isinstance(value, (int, float)):
                normalized_value = min(1.0, max(0.0, float(value)))
                model.feature_weights[feature] += weight_factor * normalized_value
            elif isinstance(value, bool):
                model.feature_weights[feature] += weight_factor if value else -weight_factor * 0.5
            elif isinstance(value, str):
                # Handle string features (convert to numeric if possible)
                try:
                    numeric_value = float(value)
                    normalized_value = min(1.0, max(0.0, numeric_value))
                    model.feature_weights[feature] += weight_factor * normalized_value
                except ValueError:
                    # For categorical strings, use hash-based approach
                    hash_value = abs(hash(value)) % 100 / 100.0
                    model.feature_weights[feature] += weight_factor * hash_value

    def _update_confidence_adjustments(self, model: LearningModel, interaction: Dict[str, Any]):
        """Update confidence adjustments based on interaction"""

        command = interaction["command"]
        action = interaction["action"]
        confidence = interaction["features"].get("confidence", 0.5)

        if command not in model.confidence_adjustments:
            model.confidence_adjustments[command] = 0.0

        # Adjust confidence threshold based on user action
        if action == "executed" and confidence < 0.8:
            # User accepted lower confidence suggestion - decrease threshold
            model.confidence_adjustments[command] -= 0.02
        elif action == "rejected" and confidence > 0.7:
            # User rejected higher confidence suggestion - increase threshold
            model.confidence_adjustments[command] += 0.02

        # Clamp adjustments to reasonable range
        model.confidence_adjustments[command] = max(-0.3, min(0.3, model.confidence_adjustments[command]))

    def _update_temporal_patterns(self, model: LearningModel, interaction: Dict[str, Any]):
        """Update temporal patterns based on interaction"""

        command = interaction["command"]
        action = interaction["action"]
        timestamp = datetime.fromisoformat(interaction["timestamp"])
        hour = timestamp.hour

        if command not in model.temporal_patterns:
            model.temporal_patterns[command] = [50] * 24  # Initialize with neutral scores

        # Ensure we have 24 hours
        if len(model.temporal_patterns[command]) < 24:
            model.temporal_patterns[command].extend([50] * (24 - len(model.temporal_patterns[command])))

        # Update temporal score for this hour
        current_score = model.temporal_patterns[command][hour]

        if action == "executed":
            new_score = min(100, current_score + 5)
        elif action == "rejected":
            new_score = max(0, current_score - 3)
        else:
            new_score = current_score  # No change for deferred

        model.temporal_patterns[command][hour] = new_score

    def _update_success_predictors(self, model: LearningModel, interaction: Dict[str, Any]):
        """Update success predictors based on interaction"""

        action = interaction["action"]
        outcome = interaction["outcome"]

        # Update success predictors based on outcome
        success = outcome.get("success", False) if action == "executed" else None

        if success is not None:
            predictor_key = f"{interaction['command']}_success"

            if predictor_key not in model.success_predictors:
                model.success_predictors[predictor_key] = 0.5

            # Update success predictor
            current_predictor = model.success_predictors[predictor_key]
            update_factor = 0.1

            if success:
                model.success_predictors[predictor_key] = current_predictor + (1.0 - current_predictor) * update_factor
            else:
                model.success_predictors[predictor_key] = current_predictor * (1.0 - update_factor)

    def _retrain_model(self, user_id: str, model: LearningModel) -> float:
        """Retrain model and return new accuracy"""

        # Mock implementation - would perform actual model training
        interactions = self.interaction_history.get(user_id, [])

        if len(interactions) < 10:
            return 0.6  # Low accuracy with few interactions

        # Simulate accuracy improvement with more data
        base_accuracy = 0.5
        data_bonus = min(0.3, len(interactions) * 0.01)
        consistency_bonus = self._calculate_interaction_consistency(interactions) * 0.2

        return min(0.95, base_accuracy + data_bonus + consistency_bonus)

    def _calculate_confidence_adjustment(self, user_id: str, command: str,
                                       context: Dict[str, Any]) -> float:
        """Calculate confidence adjustment based on learned preferences"""

        model_key = f"user_{user_id}"
        if model_key not in self.learning_models:
            return 0.0

        model = self.learning_models[model_key]

        # Get command-specific adjustments
        command_adjustment = model.confidence_adjustments.get(command, 0.0)

        # Calculate feature-based adjustments
        features = self._extract_features(context)
        feature_adjustment = 0.0

        for feature, value in features.items():
            if feature in model.feature_weights:
                if isinstance(value, (int, float)):
                    feature_adjustment += model.feature_weights[feature] * (float(value) - 0.5)
                elif isinstance(value, bool):
                    feature_adjustment += model.feature_weights[feature] * (1.0 if value else -0.5)
                elif isinstance(value, str):
                    # Handle string features
                    try:
                        numeric_value = float(value)
                        feature_adjustment += model.feature_weights[feature] * (numeric_value - 0.5)
                    except ValueError:
                        # For categorical strings, use normalized hash
                        hash_value = abs(hash(value)) % 100 / 100.0
                        feature_adjustment += model.feature_weights[feature] * (hash_value - 0.5)

        # Apply dampening to prevent extreme adjustments
        total_adjustment = (command_adjustment + feature_adjustment) * 0.3

        return max(-0.4, min(0.4, total_adjustment))  # Cap between -40% and +40%

    def _get_temporal_adjustment(self, user_id: str, command: str) -> float:
        """Get temporal adjustment based on time patterns"""

        model_key = f"user_{user_id}"
        if model_key not in self.learning_models:
            return 0.0

        model = self.learning_models[model_key]
        current_hour = datetime.now().hour

        if command in model.temporal_patterns:
            hour_scores = model.temporal_patterns[command]
            if len(hour_scores) > current_hour:
                normalized_score = (hour_scores[current_hour] - 50) / 100.0  # Normalize to -0.5 to +0.5
                return normalized_score * 0.2  # Apply temporal factor

        return 0.0

    def _assess_command_complexity(self, command: str) -> str:
        """Assess command complexity level"""

        complex_commands = ["fundamental_analysis", "architect", "product_owner"]
        simple_commands = ["social_media_content", "twitter_post"]

        if command in complex_commands:
            return "high"
        elif command in simple_commands:
            return "low"
        else:
            return "medium"

    def _create_new_learning_model(self) -> LearningModel:
        """Create new learning model for user"""

        return LearningModel(
            feature_weights={},
            confidence_adjustments={},
            temporal_patterns={},
            success_predictors={},
            model_accuracy=0.5,
            training_samples=0,
            last_trained=datetime.now()
        )

    def _load_learning_models(self) -> Dict[str, LearningModel]:
        """Load existing learning models"""

        models = {}

        for model_file in self.models_path.glob("user_*.json"):
            try:
                with open(model_file, 'r') as f:
                    model_data = json.load(f)

                # Convert datetime strings back to datetime objects
                model_data["last_trained"] = datetime.fromisoformat(model_data["last_trained"])

                models[model_file.stem] = LearningModel(**model_data)
            except Exception as e:
                print(f"Error loading model {model_file}: {e}")

        return models

    def _save_learning_model(self, model_key: str, model: LearningModel):
        """Save learning model to disk"""

        model_file = self.models_path / f"{model_key}.json"

        with open(model_file, 'w') as f:
            json.dump(asdict(model), f, indent=2, default=str)

    def _load_interaction_history(self):
        """Load interaction history from storage"""

        history_path = self.learning_path / "interactions"
        history_path.mkdir(exist_ok=True)

        for history_file in history_path.glob("user_*.json"):
            try:
                user_id = history_file.stem.replace("user_", "")
                with open(history_file, 'r') as f:
                    interactions = json.load(f)
                self.interaction_history[user_id] = interactions
            except Exception as e:
                print(f"Error loading interaction history {history_file}: {e}")

    def _save_learning_data(self, user_id: str, interaction: Dict[str, Any],
                          patterns: List[UserInteractionPattern],
                          adaptations: List[Dict[str, Any]]):
        """Save learning data to storage"""

        # Save interaction history
        history_path = self.learning_path / "interactions"
        history_path.mkdir(exist_ok=True)

        history_file = history_path / f"user_{user_id}.json"
        with open(history_file, 'w') as f:
            json.dump(self.interaction_history[user_id], f, indent=2, default=str)

        # Save patterns
        patterns_file = self.patterns_path / f"user_{user_id}_patterns.json"
        patterns_data = [asdict(pattern) for pattern in patterns]
        with open(patterns_file, 'w') as f:
            json.dump(patterns_data, f, indent=2, default=str)

        # Save adaptations
        adaptations_file = self.learning_path / "adaptations" / f"user_{user_id}_adaptations.json"
        adaptations_file.parent.mkdir(exist_ok=True)
        with open(adaptations_file, 'w') as f:
            json.dump(adaptations, f, indent=2, default=str)

    def _calculate_learning_confidence(self, user_id: str) -> float:
        """Calculate confidence in learning predictions for user"""

        interactions = self.interaction_history.get(user_id, [])

        if len(interactions) < 3:
            return 0.3  # Low confidence with few interactions

        # Calculate based on interaction consistency and volume
        consistency_score = self._calculate_interaction_consistency(interactions)
        volume_score = min(1.0, len(interactions) / 20)  # Max confidence at 20+ interactions

        return (consistency_score * 0.7 + volume_score * 0.3)

    def _calculate_interaction_consistency(self, interactions: List[Dict[str, Any]]) -> float:
        """Calculate consistency of user interactions"""

        if len(interactions) < 2:
            return 0.5

        # Group by command and calculate consistency
        command_groups = defaultdict(list)
        for interaction in interactions:
            command_groups[interaction["command"]].append(interaction["action"])

        consistency_scores = []
        for command, actions in command_groups.items():
            if len(actions) > 1:
                most_common_action = max(set(actions), key=actions.count)
                consistency = actions.count(most_common_action) / len(actions)
                consistency_scores.append(consistency)

        return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0.5

    def _calculate_learning_metrics(self, user_id: str) -> Dict[str, Any]:
        """Calculate learning metrics for user"""

        interactions = self.interaction_history.get(user_id, [])

        if not interactions:
            return {"status": "no_data"}

        total_interactions = len(interactions)
        unique_commands = len(set(i["command"] for i in interactions))
        execution_rate = len([i for i in interactions if i["action"] == "executed"]) / total_interactions

        return {
            "total_interactions": total_interactions,
            "unique_commands": unique_commands,
            "execution_rate": execution_rate,
            "learning_confidence": self._calculate_learning_confidence(user_id)
        }

    def _identify_strong_preferences(self, user_id: str) -> List[Dict[str, Any]]:
        """Identify strong user preferences"""

        interactions = self.interaction_history.get(user_id, [])
        preferences = []

        # Group by command
        command_groups = defaultdict(list)
        for interaction in interactions:
            command_groups[interaction["command"]].append(interaction)

        for command, cmd_interactions in command_groups.items():
            if len(cmd_interactions) >= 3:
                executed_count = len([i for i in cmd_interactions if i["action"] == "executed"])
                execution_rate = executed_count / len(cmd_interactions)

                if execution_rate > 0.8:
                    preferences.append({
                        "command": command,
                        "preference_type": "high_acceptance",
                        "strength": execution_rate,
                        "sample_size": len(cmd_interactions)
                    })
                elif execution_rate < 0.2:
                    preferences.append({
                        "command": command,
                        "preference_type": "low_acceptance",
                        "strength": 1 - execution_rate,
                        "sample_size": len(cmd_interactions)
                    })

        return preferences

    def _analyze_temporal_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze temporal patterns in user behavior"""

        interactions = self.interaction_history.get(user_id, [])

        if not interactions:
            return {"status": "no_data"}

        # Group by hour
        hourly_activity = defaultdict(int)
        for interaction in interactions:
            timestamp = datetime.fromisoformat(interaction["timestamp"])
            hourly_activity[timestamp.hour] += 1

        # Find peak activity hours
        if hourly_activity:
            peak_hour = max(hourly_activity.items(), key=lambda x: x[1])
            return {
                "peak_activity_hour": peak_hour[0],
                "peak_activity_count": peak_hour[1],
                "total_hours_active": len(hourly_activity),
                "activity_distribution": dict(hourly_activity)
            }

        return {"status": "no_temporal_data"}

    def _calculate_prediction_accuracy(self, user_id: str) -> float:
        """Calculate prediction accuracy for user"""

        # Mock implementation - would compare predictions to actual user actions
        interactions = self.interaction_history.get(user_id, [])

        if len(interactions) < 5:
            return 0.5  # No confidence in accuracy with few interactions

        # Simulate accuracy calculation
        return 0.78  # Simulated 78% accuracy

    def _assess_personalization_effectiveness(self, user_id: str) -> float:
        """Assess effectiveness of personalization for user"""

        interactions = self.interaction_history.get(user_id, [])

        if not interactions:
            return 0.0

        # Calculate improvement over time
        if len(interactions) >= 6:
            early_interactions = interactions[:len(interactions)//2]
            recent_interactions = interactions[len(interactions)//2:]

            early_execution_rate = len([i for i in early_interactions if i["action"] == "executed"]) / len(early_interactions)
            recent_execution_rate = len([i for i in recent_interactions if i["action"] == "executed"]) / len(recent_interactions)

            improvement = recent_execution_rate - early_execution_rate
            return max(0.0, min(1.0, 0.5 + improvement))  # Normalize to 0-1 range

        return 0.5  # Neutral effectiveness with insufficient data

    def _generate_learning_recommendations(self, user_id: str) -> List[str]:
        """Generate recommendations for improving learning"""

        interactions = self.interaction_history.get(user_id, [])
        recommendations = []

        if len(interactions) < 10:
            recommendations.append("Continue using the system to improve personalization accuracy")

        execution_rate = len([i for i in interactions if i["action"] == "executed"]) / len(interactions) if interactions else 0

        if execution_rate < 0.3:
            recommendations.append("Consider adjusting confidence thresholds to see more relevant suggestions")
        elif execution_rate > 0.9:
            recommendations.append("Enable automation for frequently accepted suggestion types")

        return recommendations

    def _get_user_patterns(self, user_id: str, command: str) -> List[UserInteractionPattern]:
        """Get user patterns for specific command"""

        patterns_file = self.patterns_path / f"user_{user_id}_patterns.json"

        if patterns_file.exists():
            try:
                with open(patterns_file, 'r') as f:
                    patterns_data = json.load(f)

                patterns = []
                for pattern_data in patterns_data:
                    if pattern_data["command"] == command:
                        pattern_data["last_updated"] = datetime.fromisoformat(pattern_data["last_updated"])
                        patterns.append(UserInteractionPattern(**pattern_data))

                return patterns
            except Exception as e:
                print(f"Error loading patterns: {e}")

        return []

    def get_learning_metrics(self) -> Dict[str, Any]:
        """Get overall learning system metrics"""

        total_users = len(self.learning_models)
        total_interactions = sum(len(interactions) for interactions in self.interaction_history.values())

        if total_users == 0:
            return {"status": "no_users", "total_interactions": 0}

        # Calculate average model accuracy
        avg_accuracy = statistics.mean(model.model_accuracy for model in self.learning_models.values())

        # Calculate learning effectiveness
        effectiveness_scores = []
        for user_id in self.interaction_history.keys():
            effectiveness = self._assess_personalization_effectiveness(user_id)
            if effectiveness > 0:
                effectiveness_scores.append(effectiveness)

        avg_effectiveness = statistics.mean(effectiveness_scores) if effectiveness_scores else 0.0

        return {
            "status": "active",
            "total_users": total_users,
            "total_interactions": total_interactions,
            "average_model_accuracy": avg_accuracy,
            "average_personalization_effectiveness": avg_effectiveness,
            "learning_system_health": self._assess_learning_system_health(),
            "adaptation_rates": self._calculate_adaptation_rates()
        }

    def _assess_learning_system_health(self) -> str:
        """Assess overall health of the learning system"""

        total_users = len(self.learning_models)

        if total_users == 0:
            return "inactive"

        # Check model accuracy distribution
        accuracies = [model.model_accuracy for model in self.learning_models.values()]
        avg_accuracy = sum(accuracies) / len(accuracies)

        # Check training data volume
        total_samples = sum(model.training_samples for model in self.learning_models.values())

        if avg_accuracy > 0.8 and total_samples > 50:
            return "excellent"
        elif avg_accuracy > 0.7 and total_samples > 20:
            return "good"
        elif avg_accuracy > 0.6 and total_samples > 10:
            return "fair"
        else:
            return "needs_improvement"

    def _calculate_adaptation_rates(self) -> Dict[str, float]:
        """Calculate adaptation rates for different aspects"""

        total_interactions = sum(len(interactions) for interactions in self.interaction_history.values())

        if total_interactions == 0:
            return {"confidence_adaptation": 0.0, "temporal_adaptation": 0.0, "preference_adaptation": 0.0}

        # Mock calculation - would analyze actual adaptation effectiveness
        return {
            "confidence_adaptation": 0.73,  # 73% of confidence adjustments improve accuracy
            "temporal_adaptation": 0.68,    # 68% of temporal patterns are learned correctly
            "preference_adaptation": 0.81   # 81% of preference patterns are captured
        }

class UserPatternAnalyzer:
    """Analyzes user interaction patterns to identify preferences"""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)

    def analyze_user_patterns(self, user_id: str,
                            interactions: List[Dict[str, Any]]) -> List[UserInteractionPattern]:
        """Analyze user interactions to identify patterns"""

        patterns = []

        # Group interactions by command
        command_interactions = defaultdict(list)
        for interaction in interactions:
            command_interactions[interaction["command"]].append(interaction)

        # Analyze each command's patterns
        for command, cmd_interactions in command_interactions.items():
            if len(cmd_interactions) >= 3:  # Need minimum interactions for pattern
                pattern = self._analyze_command_pattern(command, cmd_interactions)
                if pattern:
                    patterns.append(pattern)

        return patterns

    def _analyze_command_pattern(self, command: str,
                               interactions: List[Dict[str, Any]]) -> Optional[UserInteractionPattern]:
        """Analyze pattern for specific command"""

        # Calculate metrics
        executed_count = len([i for i in interactions if i["action"] == "executed"])
        success_rate = executed_count / len(interactions)

        # Extract common features
        features = self._extract_common_features(interactions)

        # Calculate average confidence threshold
        executed_interactions = [i for i in interactions if i["action"] == "executed"]
        if executed_interactions:
            confidence_threshold = statistics.mean(
                i["features"].get("confidence", 0.5) for i in executed_interactions
            )
        else:
            confidence_threshold = 0.5

        # Calculate time preference
        time_preferences = [i["features"].get("estimated_time", 60) for i in executed_interactions]
        avg_time_preference = int(statistics.mean(time_preferences)) if time_preferences else 60

        return UserInteractionPattern(
            command=command,
            context_features=features,
            user_action="executed" if success_rate > 0.5 else "rejected",
            success_rate=success_rate,
            frequency=len(interactions),
            confidence_threshold=confidence_threshold,
            time_preference=avg_time_preference,
            last_updated=datetime.now()
        )

    def _extract_common_features(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract common features from interactions"""

        features = {}

        # Find most common categorical features
        categorical_features = ["priority", "current_workflow", "output_type"]
        for feature in categorical_features:
            values = [i["features"].get(feature) for i in interactions if feature in i["features"]]
            if values:
                most_common = max(set(values), key=values.count)
                features[feature] = most_common

        # Calculate average numerical features
        numerical_features = ["estimated_time", "confidence"]
        for feature in numerical_features:
            values = []
            for i in interactions:
                if feature in i["features"]:
                    value = i["features"][feature]
                    if isinstance(value, (int, float)):
                        values.append(float(value))
                    elif isinstance(value, str):
                        try:
                            values.append(float(value))
                        except ValueError:
                            pass  # Skip non-numeric strings
            if values:
                features[feature] = statistics.mean(values)

        return features

class PreferencePredictor:
    """Predicts user preferences for workflow suggestions"""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)

    def predict_acceptance(self, user_id: str, command: str, features: Dict[str, Any],
                         patterns: List[UserInteractionPattern]) -> float:
        """Predict probability that user will accept suggestion"""

        # Find relevant patterns
        relevant_patterns = [p for p in patterns if p.command == command]

        if not relevant_patterns:
            return 0.5  # Default neutral probability

        pattern = relevant_patterns[0]  # Use most recent pattern

        # Base probability from success rate
        base_probability = pattern.success_rate

        # Adjust based on confidence threshold
        suggested_confidence = features.get("confidence", 0.5)
        if suggested_confidence >= pattern.confidence_threshold:
            confidence_bonus = (suggested_confidence - pattern.confidence_threshold) * 0.5
        else:
            confidence_penalty = (pattern.confidence_threshold - suggested_confidence) * 0.8
            confidence_bonus = -confidence_penalty

        # Adjust based on time preference
        suggested_time = features.get("estimated_time", 60)
        if suggested_time <= pattern.time_preference:
            time_bonus = (pattern.time_preference - suggested_time) / pattern.time_preference * 0.3
        else:
            time_penalty = (suggested_time - pattern.time_preference) / suggested_time * 0.4
            time_bonus = -time_penalty

        # Calculate final probability
        final_probability = base_probability + confidence_bonus + time_bonus

        return max(0.0, min(1.0, final_probability))

    def predict_optimal_parameters(self, user_id: str, command: str,
                                 features: Dict[str, Any],
                                 patterns: List[UserInteractionPattern]) -> Dict[str, Any]:
        """Predict optimal parameters for user satisfaction"""

        relevant_patterns = [p for p in patterns if p.command == command]

        if not relevant_patterns:
            return {"confidence_threshold": 0.7, "max_time": 120}

        pattern = relevant_patterns[0]

        return {
            "confidence_threshold": pattern.confidence_threshold,
            "max_time": pattern.time_preference,
            "preferred_priority": pattern.context_features.get("priority", "medium"),
            "optimal_context": pattern.context_features
        }

class AdaptationEngine:
    """Generates adaptive recommendations based on learned patterns"""

    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)

    def generate_adaptations(self, user_id: str,
                           patterns: List[UserInteractionPattern]) -> List[Dict[str, Any]]:
        """Generate adaptation recommendations"""

        adaptations = []

        for pattern in patterns:
            # Confidence threshold adaptations
            if pattern.success_rate > 0.8 and pattern.confidence_threshold < 0.6:
                adaptations.append({
                    "type": "lower_confidence_threshold",
                    "command": pattern.command,
                    "current_threshold": pattern.confidence_threshold,
                    "recommended_threshold": max(0.4, pattern.confidence_threshold - 0.1),
                    "reason": "High success rate with lower confidence suggestions"
                })

            # Time preference adaptations
            if pattern.success_rate > 0.7 and pattern.time_preference > 180:
                adaptations.append({
                    "type": "increase_time_tolerance",
                    "command": pattern.command,
                    "current_preference": pattern.time_preference,
                    "recommended_preference": pattern.time_preference + 60,
                    "reason": "User accepts longer workflows for this command"
                })

            # Automation recommendations
            if pattern.success_rate > 0.9 and pattern.frequency > 10:
                adaptations.append({
                    "type": "enable_automation",
                    "command": pattern.command,
                    "automation_threshold": pattern.confidence_threshold + 0.1,
                    "reason": "Very high success rate suggests automation readiness"
                })

        return adaptations
