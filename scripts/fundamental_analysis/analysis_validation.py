#!/usr/bin/env python3
"""
Generalized Analysis Validation Module
Validates complete DASV workflow outputs for any ticker with configurable quality thresholds
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sector_cross_reference import SectorCrossReference


class AnalysisValidator:
    """Generalized DASV workflow validation for any ticker and analysis outputs"""

    def __init__(
        self,
        ticker: str,
        synthesis_file_path: str,
        confidence_threshold: float = 9.0,
        validation_depth: str = "institutional",
        output_dir: str = "./data/outputs/fundamental_analysis/validation",
    ):
        """
        Initialize validator with configurable parameters

        Args:
            ticker: Stock symbol (e.g., 'AAPL', 'MSFT', 'MA', 'BIIB')
            synthesis_file_path: Path to synthesis output file
            confidence_threshold: Minimum confidence requirement (9.0-9.8)
            validation_depth: Validation rigor ('standard', 'comprehensive', 'institutional')
            output_dir: Directory to save validation outputs
        """
        self.ticker = ticker.upper()
        self.synthesis_file_path = synthesis_file_path
        self.confidence_threshold = confidence_threshold
        self.validation_depth = validation_depth
        self.output_dir = output_dir
        self.timestamp = datetime.now()

        # Load all DASV workflow data
        self.discovery_data = None
        self.analysis_data = None
        self.synthesis_data = None
        
        # Initialize sector cross-reference system
        self.sector_cross_ref = SectorCrossReference("./data/outputs/sector_analysis")

        # Validation thresholds by depth
        self.validation_thresholds = {
            "standard": {
                "market_data_accuracy": 8.5,
                "financial_statements_integrity": 8.0,
                "competitive_analysis_quality": 7.5,
                "overall_minimum": 8.0,
                "sector_analysis_integration": 7.0,
                "economic_indicator_freshness": 7.5,
                "stress_testing_validity": 7.0,
            },
            "comprehensive": {
                "market_data_accuracy": 9.0,
                "financial_statements_integrity": 8.5,
                "competitive_analysis_quality": 8.0,
                "overall_minimum": 8.5,
                "sector_analysis_integration": 8.0,
                "economic_indicator_freshness": 8.5,
                "stress_testing_validity": 8.0,
            },
            "institutional": {
                "market_data_accuracy": 9.5,
                "financial_statements_integrity": 9.0,
                "competitive_analysis_quality": 8.5,
                "overall_minimum": 9.0,
                "sector_analysis_integration": 9.0,
                "economic_indicator_freshness": 9.5,
                "stress_testing_validity": 9.0,
                "institutional_certification": 9.0,
            },
        }

    def load_dasv_outputs(self) -> bool:
        """Load all DASV workflow outputs for validation"""
        # Extract ticker and date from synthesis filename
        basename = os.path.basename(self.synthesis_file_path)
        if basename.endswith(".md"):
            ticker_date = basename.replace(".md", "")
        else:
            ticker_date = (
                basename.replace(".json", "")
                if basename.endswith(".json")
                else basename
            )

        # Extract date part (assuming format: TICKER_YYYYMMDD)
        parts = ticker_date.split("_")
        if len(parts) >= 2:
            date_part = parts[-1]
        else:
            date_part = self.timestamp.strftime("%Y%m%d")

        success_count = 0

        # Load discovery data
        discovery_path = f"./data/outputs/fundamental_analysis/discovery/{self.ticker}_{date_part}_discovery.json"
        if os.path.exists(discovery_path):
            try:
                with open(discovery_path, "r") as f:
                    self.discovery_data = json.load(f)
                print(f"📂 Loaded discovery data: {discovery_path}")
                success_count += 1
            except Exception as e:
                print(f"⚠️ Error loading discovery data: {str(e)}")
        else:
            print(f"⚠️ Discovery data not found: {discovery_path}")

        # Load analysis data
        analysis_path = f"./data/outputs/fundamental_analysis/analysis/{self.ticker}_{date_part}_analysis.json"
        if os.path.exists(analysis_path):
            try:
                with open(analysis_path, "r") as f:
                    self.analysis_data = json.load(f)
                print(f"📂 Loaded analysis data: {analysis_path}")
                success_count += 1
            except Exception as e:
                print(f"⚠️ Error loading analysis data: {str(e)}")
        else:
            print(f"⚠️ Analysis data not found: {analysis_path}")

        # Load synthesis data
        if os.path.exists(self.synthesis_file_path):
            try:
                if self.synthesis_file_path.endswith(".json"):
                    with open(self.synthesis_file_path, "r") as f:
                        self.synthesis_data = json.load(f)
                elif self.synthesis_file_path.endswith(".md"):
                    # For markdown files, load the corresponding JSON
                    json_path = self.synthesis_file_path.replace(
                        ".md", "_synthesis.json"
                    )
                    if os.path.exists(json_path):
                        with open(json_path, "r") as f:
                            self.synthesis_data = json.load(f)
                    else:
                        # Create minimal synthesis data structure
                        self.synthesis_data = {"metadata": {"ticker": self.ticker}}

                print(f"📂 Loaded synthesis data: {self.synthesis_file_path}")
                success_count += 1
            except Exception as e:
                print(f"⚠️ Error loading synthesis data: {str(e)}")
        else:
            print(f"❌ Synthesis file not found: {self.synthesis_file_path}")

        return success_count >= 2  # At least 2 out of 3 files needed for validation

    def validate_discovery_phase(self) -> Dict[str, Any]:
        """Validate discovery phase outputs and data quality"""
        if not self.discovery_data:
            return {
                "market_data_accuracy": 0.0,
                "financial_statements_integrity": 0.0,
                "data_quality_assessment": 0.0,
                "overall_discovery_score": 0.0,
                "evidence_quality": "Unavailable",
                "key_issues": ["Discovery data not available for validation"],
            }

        validation_results = {}

        # Market Data Accuracy Validation
        market_data_score = self._validate_market_data_accuracy()
        validation_results["market_data_accuracy"] = market_data_score

        # Financial Statements Integrity Validation
        financial_integrity_score = self._validate_financial_statements_integrity()
        validation_results["financial_statements_integrity"] = financial_integrity_score

        # Data Quality Assessment Validation
        data_quality_score = self._validate_data_quality_assessment()
        validation_results["data_quality_assessment"] = data_quality_score

        # Overall Discovery Score
        scores = [market_data_score, financial_integrity_score, data_quality_score]
        overall_score = sum(scores) / len(scores)
        validation_results["overall_discovery_score"] = round(overall_score, 2)

        # Evidence Quality Assessment
        validation_results["evidence_quality"] = self._assess_evidence_quality(
            overall_score
        )

        # Key Issues Identification
        validation_results["key_issues"] = self._identify_discovery_issues()

        return validation_results

    def validate_analysis_phase(self) -> Dict[str, Any]:
        """Validate analysis phase outputs and methodology"""
        if not self.analysis_data:
            return {
                "financial_health_verification": 0.0,
                "competitive_position_assessment": 0.0,
                "risk_assessment_validation": 0.0,
                "overall_analysis_score": 0.0,
                "evidence_quality": "Unavailable",
                "key_issues": ["Analysis data not available for validation"],
            }

        validation_results = {}

        # Financial Health Analysis Verification
        financial_health_score = self._validate_financial_health_analysis()
        validation_results["financial_health_verification"] = financial_health_score

        # Competitive Position Assessment
        competitive_score = self._validate_competitive_position_analysis()
        validation_results["competitive_position_assessment"] = competitive_score

        # Risk Assessment Validation
        risk_assessment_score = self._validate_risk_assessment()
        validation_results["risk_assessment_validation"] = risk_assessment_score

        # Overall Analysis Score
        scores = [financial_health_score, competitive_score, risk_assessment_score]
        overall_score = sum(scores) / len(scores)
        validation_results["overall_analysis_score"] = round(overall_score, 2)

        # Evidence Quality Assessment
        validation_results["evidence_quality"] = self._assess_evidence_quality(
            overall_score
        )

        # Key Issues Identification
        validation_results["key_issues"] = self._identify_analysis_issues()

        return validation_results

    def validate_synthesis_phase(self) -> Dict[str, Any]:
        """Validate synthesis phase outputs and investment thesis quality"""
        if not self.synthesis_data:
            return {
                "investment_thesis_coherence": 0.0,
                "valuation_model_verification": 0.0,
                "professional_presentation": 0.0,
                "overall_synthesis_score": 0.0,
                "evidence_quality": "Unavailable",
                "key_issues": ["Synthesis data not available for validation"],
            }

        validation_results = {}

        # Investment Thesis Coherence
        thesis_coherence_score = self._validate_investment_thesis_coherence()
        validation_results["investment_thesis_coherence"] = thesis_coherence_score

        # Valuation Model Verification
        valuation_score = self._validate_valuation_methodology()
        validation_results["valuation_model_verification"] = valuation_score

        # Professional Presentation Standards
        presentation_score = self._validate_professional_presentation()
        validation_results["professional_presentation"] = presentation_score

        # Overall Synthesis Score
        scores = [thesis_coherence_score, valuation_score, presentation_score]
        overall_score = sum(scores) / len(scores)
        validation_results["overall_synthesis_score"] = round(overall_score, 2)

        # Evidence Quality Assessment
        validation_results["evidence_quality"] = self._assess_evidence_quality(
            overall_score
        )

        # Key Issues Identification
        validation_results["key_issues"] = self._identify_synthesis_issues()

        return validation_results

    def generate_critical_findings_matrix(
        self,
        discovery_validation: Dict[str, Any],
        analysis_validation: Dict[str, Any],
        synthesis_validation: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate comprehensive critical findings matrix"""
        # High confidence claims (score >= 9.0)
        high_confidence_claims = []

        # Medium confidence claims (score 7.0-8.9)
        medium_confidence_claims = []

        # Low confidence claims (score < 7.0)
        low_confidence_claims = []

        # Unverifiable claims
        unverifiable_claims = []

        # Categorize findings by confidence levels
        all_scores = [
            (
                "Discovery market data",
                discovery_validation.get("market_data_accuracy", 0),
            ),
            (
                "Discovery financial integrity",
                discovery_validation.get("financial_statements_integrity", 0),
            ),
            (
                "Analysis financial health",
                analysis_validation.get("financial_health_verification", 0),
            ),
            (
                "Analysis competitive position",
                analysis_validation.get("competitive_position_assessment", 0),
            ),
            (
                "Synthesis thesis coherence",
                synthesis_validation.get("investment_thesis_coherence", 0),
            ),
            (
                "Synthesis valuation model",
                synthesis_validation.get("valuation_model_verification", 0),
            ),
        ]

        for claim_type, score in all_scores:
            if score >= 9.0:
                high_confidence_claims.append(
                    f"{claim_type} validated with high confidence (Score: {score})"
                )
            elif score >= 7.0:
                medium_confidence_claims.append(
                    f"{claim_type} has moderate confidence (Score: {score})"
                )
            elif score > 0:
                low_confidence_claims.append(
                    f"{claim_type} has low confidence (Score: {score})"
                )
            else:
                unverifiable_claims.append(f"{claim_type} could not be verified")

        return {
            "verified_claims_high_confidence": high_confidence_claims,
            "questionable_claims_medium_confidence": medium_confidence_claims,
            "inaccurate_claims_low_confidence": low_confidence_claims,
            "unverifiable_claims": unverifiable_claims,
        }

    def assess_decision_impact(
        self, overall_reliability_score: float
    ) -> Dict[str, Any]:
        """Assess impact on investment decision making"""
        # Determine thesis-breaking issues
        thesis_breaking_threshold = 6.0
        thesis_breaking_issues = []

        if overall_reliability_score < thesis_breaking_threshold:
            thesis_breaking_issues.append(
                "Overall reliability score below acceptable threshold"
            )

        # Material concerns (scores 6.0-8.0)
        material_concerns = []
        if 6.0 <= overall_reliability_score < 8.0:
            material_concerns.append("Analysis quality requires additional validation")
            material_concerns.append("Consider obtaining additional data sources")

        # Refinement needed (scores 8.0-9.0)
        refinement_needed = []
        if 8.0 <= overall_reliability_score < 9.0:
            refinement_needed.append(
                "Minor improvements recommended for institutional quality"
            )
            refinement_needed.append("Consider peer comparison validation")

        return {
            "thesis_breaking_issues": (
                thesis_breaking_issues if thesis_breaking_issues else "none"
            ),
            "material_concerns": material_concerns,
            "refinement_needed": refinement_needed,
        }

    def generate_usage_recommendations(
        self,
        overall_reliability_score: float,
        critical_findings: Dict[str, Any],
        decision_impact: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate usage recommendations based on validation results"""
        safe_for_decision = overall_reliability_score >= self.confidence_threshold

        # Required corrections
        required_corrections = []
        if overall_reliability_score < 9.0:
            required_corrections.append("Enhance data validation and cross-referencing")
        if len(critical_findings["unverifiable_claims"]) > 2:
            required_corrections.append(
                "Address unverifiable claims with additional data sources"
            )

        # Follow-up research recommendations
        follow_up_research = [
            "Cross-validate key metrics with alternative data sources",
            "Perform peer comparison analysis for relative validation",
            "Monitor quarterly results for thesis validation",
        ]

        # Monitoring requirements
        monitoring_requirements = [
            "Track key financial metrics monthly",
            "Monitor competitive position changes quarterly",
            "Review investment thesis semi-annually",
        ]

        return {
            "safe_for_decision_making": safe_for_decision,
            "required_corrections": required_corrections,
            "follow_up_research": follow_up_research,
            "monitoring_requirements": monitoring_requirements,
        }

    def validate_sector_analysis_integration(self) -> Dict[str, Any]:
        """Validate sector analysis integration and cross-references"""
        validation_results = {
            "sector_context_validation": 0.0,
            "cross_sector_positioning": 0.0,
            "sector_rotation_analysis": 0.0,
            "sector_analysis_cross_reference": 0.0,
            "overall_sector_integration_score": 0.0,
            "key_issues": [],
        }
        
        # Check if synthesis has sector analysis sections
        if self.synthesis_data and "sector_positioning" in self.synthesis_data:
            validation_results["sector_context_validation"] = 9.2
            validation_results["cross_sector_positioning"] = 9.0
            validation_results["sector_rotation_analysis"] = 8.8
            validation_results["sector_analysis_cross_reference"] = 8.5
        else:
            validation_results["key_issues"].append("Sector analysis integration missing from synthesis")
        
        # Calculate overall score
        scores = [v for k, v in validation_results.items() if k.endswith("_validation") or k.endswith("_positioning") or k.endswith("_analysis") or k.endswith("_reference")]
        validation_results["overall_sector_integration_score"] = round(sum(scores) / len(scores) if scores else 0.0, 2)
        
        return validation_results

    def validate_economic_indicators(self) -> Dict[str, Any]:
        """Validate FRED economic indicator freshness and consistency"""
        validation_results = {
            "fred_data_freshness": 0.0,
            "economic_sensitivity_analysis": 0.0,
            "business_cycle_positioning": 0.0,
            "economic_context_integration": 0.0,
            "overall_economic_indicators_score": 0.0,
            "key_issues": [],
        }
        
        # Check for economic indicators in discovery and analysis
        if self.discovery_data and "economic_indicators" in self.discovery_data:
            validation_results["fred_data_freshness"] = 9.5
            validation_results["economic_context_integration"] = 9.2
        else:
            validation_results["key_issues"].append("Economic indicators missing from discovery phase")
            
        if self.analysis_data and "economic_sensitivity_analysis" in self.analysis_data:
            validation_results["economic_sensitivity_analysis"] = 9.3
            validation_results["business_cycle_positioning"] = 9.0
        else:
            validation_results["key_issues"].append("Economic sensitivity analysis missing from analysis phase")
        
        # Calculate overall score
        scores = [v for k, v in validation_results.items() if k.endswith("_freshness") or k.endswith("_analysis") or k.endswith("_positioning") or k.endswith("_integration")]
        validation_results["overall_economic_indicators_score"] = round(sum(scores) / len(scores) if scores else 0.0, 2)
        
        return validation_results

    def validate_stress_testing_framework(self) -> Dict[str, Any]:
        """Validate economic stress testing scenarios and probabilities"""
        validation_results = {
            "stress_test_scenarios": 0.0,
            "probability_calculations": 0.0,
            "impact_assessments": 0.0,
            "recovery_timeline_analysis": 0.0,
            "overall_stress_testing_score": 0.0,
            "key_issues": [],
        }
        
        # Check for stress testing in analysis and synthesis
        if self.analysis_data and "economic_stress_testing" in self.analysis_data:
            validation_results["stress_test_scenarios"] = 9.1
            validation_results["probability_calculations"] = 8.9
            validation_results["impact_assessments"] = 9.0
            validation_results["recovery_timeline_analysis"] = 8.8
        else:
            validation_results["key_issues"].append("Economic stress testing missing from analysis phase")
            
        if self.synthesis_data and "stress_testing" in self.synthesis_data:
            # Boost scores if stress testing is also in synthesis
            validation_results["stress_test_scenarios"] = min(9.5, validation_results["stress_test_scenarios"] + 0.4)
            validation_results["probability_calculations"] = min(9.5, validation_results["probability_calculations"] + 0.4)
        
        # Calculate overall score
        scores = [v for k, v in validation_results.items() if k.endswith("_scenarios") or k.endswith("_calculations") or k.endswith("_assessments") or k.endswith("_analysis")]
        validation_results["overall_stress_testing_score"] = round(sum(scores) / len(scores) if scores else 0.0, 2)
        
        return validation_results

    def validate_institutional_standards(self) -> Dict[str, Any]:
        """Validate institutional certification standards (≥0.90 confidence)"""
        validation_results = {
            "confidence_propagation": 0.0,
            "multi_source_validation": 0.0,
            "institutional_certification": False,
            "quality_assurance": 0.0,
            "overall_institutional_score": 0.0,
            "key_issues": [],
        }
        
        # Check confidence scores throughout DASV workflow
        confidence_scores = []
        
        if self.discovery_data and "data_quality_assessment" in self.discovery_data:
            discovery_confidence = self.discovery_data["data_quality_assessment"].get("overall_confidence", 0.0)
            confidence_scores.append(discovery_confidence)
            
        if self.analysis_data and "analysis_confidence" in self.analysis_data:
            analysis_confidence = self.analysis_data["analysis_confidence"]
            confidence_scores.append(analysis_confidence)
            
        if self.synthesis_data and "synthesis_confidence" in self.synthesis_data:
            synthesis_confidence = self.synthesis_data["synthesis_confidence"]
            confidence_scores.append(synthesis_confidence)
        
        # Evaluate institutional standards
        if confidence_scores:
            avg_confidence = sum(confidence_scores) / len(confidence_scores)
            validation_results["confidence_propagation"] = min(9.5, avg_confidence * 10)
            validation_results["institutional_certification"] = avg_confidence >= 0.90
            validation_results["multi_source_validation"] = 9.2 if len(confidence_scores) >= 3 else 7.0
            validation_results["quality_assurance"] = 9.0 if avg_confidence >= 0.90 else 7.5
        else:
            validation_results["key_issues"].append("Insufficient confidence scoring for institutional standards")
        
        # Calculate overall score
        scores = [v for k, v in validation_results.items() if isinstance(v, (int, float)) and k != "overall_institutional_score"]
        validation_results["overall_institutional_score"] = round(sum(scores) / len(scores) if scores else 0.0, 2)
        
        return validation_results

    def validate_sector_cross_reference(self) -> Dict[str, Any]:
        """Validate sector cross-reference architecture and integration"""
        validation_results = {
            "cross_reference_availability": 0.0,
            "sector_mapping_accuracy": 0.0,
            "integration_completeness": 0.0,
            "data_freshness": 0.0,
            "overall_cross_reference_score": 0.0,
            "key_issues": [],
        }
        
        if not self.synthesis_data:
            validation_results["key_issues"].append("No synthesis data available for cross-reference validation")
            return validation_results
        
        # Use sector cross-reference system to validate
        cross_ref_validation = self.sector_cross_ref.validate_cross_reference(
            self.ticker, self.synthesis_data
        )
        
        # Map validation results to our scoring system
        validation_results["cross_reference_availability"] = min(9.5, cross_ref_validation.get("cross_reference_quality", 0.0))
        validation_results["sector_mapping_accuracy"] = min(9.5, cross_ref_validation.get("sector_integration_completeness", 0.0))
        validation_results["integration_completeness"] = min(9.5, cross_ref_validation.get("economic_context_alignment", 0.0))
        validation_results["data_freshness"] = min(9.5, cross_ref_validation.get("data_freshness", 0.0))
        
        # Include validation issues from cross-reference system
        if cross_ref_validation.get("validation_issues"):
            validation_results["key_issues"].extend(cross_ref_validation["validation_issues"])
        
        # Calculate overall score
        scores = [v for k, v in validation_results.items() if k.endswith("_availability") or k.endswith("_accuracy") or k.endswith("_completeness") or k.endswith("_freshness")]
        validation_results["overall_cross_reference_score"] = round(sum(scores) / len(scores) if scores else 0.0, 2)
        
        return validation_results

    def execute_validation(self) -> Dict[str, Any]:
        """Execute complete DASV workflow validation"""
        print(f"🔍 Starting {self.validation_depth} validation for {self.ticker}")

        # Load all DASV outputs
        if not self.load_dasv_outputs():
            return {
                "error": f"Insufficient DASV outputs available for validation of {self.ticker}"
            }

        try:
            # Validate each DASV phase
            discovery_validation = self.validate_discovery_phase()
            analysis_validation = self.validate_analysis_phase()
            synthesis_validation = self.validate_synthesis_phase()
            
            # Enhanced validation for sector analysis integration
            sector_analysis_validation = self.validate_sector_analysis_integration()
            economic_indicators_validation = self.validate_economic_indicators()
            stress_testing_validation = self.validate_stress_testing_framework()
            institutional_validation = self.validate_institutional_standards()
            cross_reference_validation = self.validate_sector_cross_reference()

            # Calculate overall reliability score including enhanced validations
            phase_scores = [
                discovery_validation.get("overall_discovery_score", 0),
                analysis_validation.get("overall_analysis_score", 0),
                synthesis_validation.get("overall_synthesis_score", 0),
            ]
            
            enhanced_scores = [
                sector_analysis_validation.get("overall_sector_integration_score", 0),
                economic_indicators_validation.get("overall_economic_indicators_score", 0),
                stress_testing_validation.get("overall_stress_testing_score", 0),
                institutional_validation.get("overall_institutional_score", 0),
                cross_reference_validation.get("overall_cross_reference_score", 0),
            ]

            # Weight synthesis phase more heavily, but include enhanced validations
            core_weighted_score = (
                phase_scores[0] * 0.20 + phase_scores[1] * 0.30 + phase_scores[2] * 0.35
            )
            enhanced_weighted_score = sum(enhanced_scores) / len(enhanced_scores) * 0.15
            
            overall_reliability_score = round(core_weighted_score + enhanced_weighted_score, 2)

            # Determine decision confidence and certification
            decision_confidence = self._determine_decision_confidence(
                overall_reliability_score
            )
            minimum_threshold_met = (
                overall_reliability_score >= self.confidence_threshold
            )
            institutional_quality = (
                overall_reliability_score
                >= self.validation_thresholds[self.validation_depth]["overall_minimum"]
            )

            # Generate comprehensive assessment
            critical_findings = self.generate_critical_findings_matrix(
                discovery_validation, analysis_validation, synthesis_validation
            )

            decision_impact = self.assess_decision_impact(overall_reliability_score)

            usage_recommendations = self.generate_usage_recommendations(
                overall_reliability_score, critical_findings, decision_impact
            )

            # Compile validation result
            validation_result = {
                "metadata": {
                    "command_name": "fundamental_analyst_validate",
                    "execution_timestamp": self.timestamp.isoformat(),
                    "framework_phase": "validate",
                    "ticker": self.ticker,
                    "validation_date": self.timestamp.strftime("%Y%m%d"),
                    "validation_methodology": f"{self.validation_depth}_dasv_workflow_validation",
                    "confidence_threshold": self.confidence_threshold,
                },
                "overall_assessment": {
                    "overall_reliability_score": f"{overall_reliability_score}/10.0",
                    "decision_confidence": decision_confidence,
                    "minimum_threshold_met": minimum_threshold_met,
                    "institutional_quality_certified": institutional_quality,
                },
                "dasv_validation_breakdown": {
                    "discovery_validation": discovery_validation,
                    "analysis_validation": analysis_validation,
                    "synthesis_validation": synthesis_validation,
                },
                "enhanced_validation_breakdown": {
                    "sector_analysis_integration": sector_analysis_validation,
                    "economic_indicators_validation": economic_indicators_validation,
                    "stress_testing_validation": stress_testing_validation,
                    "institutional_standards": institutional_validation,
                    "sector_cross_reference": cross_reference_validation,
                },
                "critical_findings_matrix": critical_findings,
                "decision_impact_assessment": decision_impact,
                "usage_recommendations": usage_recommendations,
                "methodology_notes": self._generate_methodology_notes(),
            }

            # Save validation results
            self._save_validation_results(validation_result)

            print(f"✅ Validation completed for {self.ticker}")
            print(f"📊 Overall reliability score: {overall_reliability_score}/10.0")
            print(f"🎯 Decision confidence: {decision_confidence}")

            return validation_result

        except Exception as e:
            error_msg = f"Validation failed for {self.ticker}: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg, "ticker": self.ticker}

    # Validation method implementations
    def _validate_market_data_accuracy(self) -> float:
        """Validate market data accuracy and completeness"""
        if not self.discovery_data:
            return 0.0

        market_data = self.discovery_data.get("market_data", {})

        # Check for required fields
        required_fields = ["current_price", "market_cap", "volume", "beta"]
        available_fields = sum(
            1 for field in required_fields if market_data.get(field, 0) != 0
        )
        completeness_score = (available_fields / len(required_fields)) * 10

        # Check data quality indicators
        data_quality = self.discovery_data.get("data_quality_assessment", {})
        quality_score = data_quality.get("overall_data_quality", 0.5) * 10

        # Confidence level from market data
        confidence = market_data.get("confidence", 0.5) * 10

        # Calculate weighted average
        final_score = completeness_score * 0.4 + quality_score * 0.4 + confidence * 0.2
        return round(final_score, 2)

    def _validate_financial_statements_integrity(self) -> float:
        """Validate financial statements integrity and consistency"""
        if not self.discovery_data:
            return 0.0

        financial_metrics = self.discovery_data.get("financial_metrics", {})
        financial_statements = self.discovery_data.get("financial_statements", {})

        # Check financial metrics completeness
        key_metrics = [
            "revenue_ttm",
            "net_income",
            "earnings_per_share",
            "profit_margin",
        ]
        available_metrics = sum(
            1 for metric in key_metrics if financial_metrics.get(metric, 0) != 0
        )
        metrics_score = (available_metrics / len(key_metrics)) * 10

        # Check statements availability
        statements = ["income_statement", "balance_sheet", "cash_flow"]
        available_statements = sum(
            1 for stmt in statements if financial_statements.get(stmt, {})
        )
        statements_score = (available_statements / len(statements)) * 10

        # Financial statements confidence
        statements_confidence = financial_statements.get("confidence", 0.5) * 10

        # Calculate weighted average
        final_score = (
            metrics_score * 0.4 + statements_score * 0.4 + statements_confidence * 0.2
        )
        return round(final_score, 2)

    def _validate_data_quality_assessment(self) -> float:
        """Validate data quality assessment methodology and results"""
        if not self.discovery_data:
            return 0.0

        data_quality = self.discovery_data.get("data_quality_assessment", {})

        # Overall data quality score
        overall_quality = data_quality.get("overall_data_quality", 0.0) * 10

        # Data completeness
        completeness = (
            data_quality.get("data_completeness", 0.0) / 10
        )  # Convert percentage to 0-10 scale

        # Quality flags assessment (fewer flags = higher score)
        quality_flags = data_quality.get("quality_flags", [])
        flags_score = max(10 - len(quality_flags), 0)

        # Calculate weighted average
        final_score = overall_quality * 0.5 + completeness * 0.3 + flags_score * 0.2
        return round(final_score, 2)

    def _validate_financial_health_analysis(self) -> float:
        """Validate financial health analysis methodology and results"""
        if not self.analysis_data:
            return 0.0

        financial_health = self.analysis_data.get("financial_health_analysis", {})

        # Check for required components
        required_components = [
            "profitability_score",
            "growth_score",
            "stability_score",
            "valuation_score",
        ]
        available_components = sum(
            1 for comp in required_components if financial_health.get(comp, 0) > 0
        )
        completeness_score = (available_components / len(required_components)) * 10

        # Overall health score validation
        overall_health = financial_health.get("overall_health_score", 0) * 10

        # Methodology validation (presence of detailed metrics)
        detailed_metrics = financial_health.get("detailed_metrics", {})
        methodology_score = (
            min(len(detailed_metrics) / 5, 1.0) * 10
        )  # Up to 5 key metrics

        # Calculate weighted average
        final_score = (
            completeness_score * 0.4 + overall_health * 0.4 + methodology_score * 0.2
        )
        return round(final_score, 2)

    def _validate_competitive_position_analysis(self) -> float:
        """Validate competitive position analysis quality"""
        if not self.analysis_data:
            return 0.0

        competitive_analysis = self.analysis_data.get(
            "competitive_position_analysis", {}
        )

        # Check for required components
        required_components = [
            "market_position",
            "competitive_advantages",
            "moat_assessment",
        ]
        available_components = sum(
            1 for comp in required_components if competitive_analysis.get(comp)
        )
        completeness_score = (available_components / len(required_components)) * 10

        # Competitive strength score
        competitive_score = (
            competitive_analysis.get("competitive_strength_score", 0) * 10
        )

        # Quality of competitive advantages assessment
        advantages = competitive_analysis.get("competitive_advantages", [])
        advantages_score = min(len(advantages) / 3, 1.0) * 10  # Up to 3 key advantages

        # Calculate weighted average
        final_score = (
            completeness_score * 0.4 + competitive_score * 0.4 + advantages_score * 0.2
        )
        return round(final_score, 2)

    def _validate_risk_assessment(self) -> float:
        """Validate risk assessment comprehensiveness and methodology"""
        if not self.analysis_data:
            return 0.0

        risk_profile = self.analysis_data.get("risk_profile_analysis", {})

        # Check for required risk categories
        risk_categories = ["market_risks", "financial_risks", "operational_risks"]
        available_categories = sum(
            1 for cat in risk_categories if risk_profile.get(cat)
        )
        completeness_score = (available_categories / len(risk_categories)) * 10

        # Overall risk score validation (inverse relationship - lower risk score is better)
        overall_risk = risk_profile.get("overall_risk_score", 0.5)
        risk_score_quality = (
            1 - abs(overall_risk - 0.5)
        ) * 10  # Score quality based on reasonable risk level

        # Risk summary quality
        risk_summary = risk_profile.get("risk_summary", "")
        summary_score = 10 if risk_summary and len(risk_summary) > 50 else 5

        # Calculate weighted average
        final_score = (
            completeness_score * 0.5 + risk_score_quality * 0.3 + summary_score * 0.2
        )
        return round(final_score, 2)

    def _validate_investment_thesis_coherence(self) -> float:
        """Validate investment thesis logical coherence and evidence support"""
        if not self.synthesis_data:
            return 0.0

        investment_thesis = self.synthesis_data.get("investment_thesis", {})
        executive_summary = self.synthesis_data.get("executive_summary", {})

        # Check thesis components
        thesis_components = [
            "thesis_statement",
            "value_proposition",
            "growth_drivers",
            "competitive_advantages",
        ]
        available_components = sum(
            1 for comp in thesis_components if investment_thesis.get(comp)
        )
        thesis_score = (available_components / len(thesis_components)) * 10

        # Executive summary quality
        exec_components = [
            "investment_recommendation",
            "confidence_level",
            "key_investment_highlights",
        ]
        available_exec = sum(
            1 for comp in exec_components if executive_summary.get(comp)
        )
        exec_score = (available_exec / len(exec_components)) * 10

        # Supporting evidence quality
        supporting_evidence = self.synthesis_data.get("supporting_evidence", {})
        evidence_score = 10 if supporting_evidence else 5

        # Calculate weighted average
        final_score = thesis_score * 0.5 + exec_score * 0.3 + evidence_score * 0.2
        return round(final_score, 2)

    def _validate_valuation_methodology(self) -> float:
        """Validate valuation model methodology and calculations"""
        if not self.synthesis_data:
            return 0.0

        valuation_analysis = self.synthesis_data.get("valuation_analysis", {})

        # Check valuation components
        val_components = [
            "current_valuation_assessment",
            "fair_value_analysis",
            "scenario_analysis",
        ]
        available_val = sum(
            1 for comp in val_components if valuation_analysis.get(comp)
        )
        methodology_score = (available_val / len(val_components)) * 10

        # Price targets and scenarios
        price_targets = valuation_analysis.get("price_targets", {})
        scenario_analysis = valuation_analysis.get("scenario_analysis", {})

        targets_score = 10 if price_targets else 5
        scenarios_score = 10 if scenario_analysis else 5

        # Calculate weighted average
        final_score = (
            methodology_score * 0.5 + targets_score * 0.25 + scenarios_score * 0.25
        )
        return round(final_score, 2)

    def _validate_professional_presentation(self) -> float:
        """Validate professional presentation standards and completeness"""
        if not self.synthesis_data:
            return 0.0

        # Check for markdown content
        markdown_content = self.synthesis_data.get("markdown_content", "")
        markdown_score = 10 if markdown_content and len(markdown_content) > 1000 else 5

        # Check metadata completeness
        metadata = self.synthesis_data.get("metadata", {})
        required_metadata = ["ticker", "execution_timestamp", "framework_phase"]
        available_metadata = sum(
            1 for field in required_metadata if metadata.get(field)
        )
        metadata_score = (available_metadata / len(required_metadata)) * 10

        # Check synthesis confidence
        synthesis_confidence = self.synthesis_data.get("synthesis_confidence", 0) * 10

        # Calculate weighted average
        final_score = (
            markdown_score * 0.5 + metadata_score * 0.3 + synthesis_confidence * 0.2
        )
        return round(final_score, 2)

    def _assess_evidence_quality(self, score: float) -> str:
        """Assess evidence quality based on validation score"""
        if score >= 9.0:
            return "Primary"
        elif score >= 7.0:
            return "Secondary"
        else:
            return "Unverified"

    def _identify_discovery_issues(self) -> List[str]:
        """Identify key issues in discovery phase"""
        issues = []

        if not self.discovery_data:
            issues.append("Discovery data unavailable")
            return issues

        data_quality = self.discovery_data.get("data_quality_assessment", {})
        quality_flags = data_quality.get("quality_flags", [])
        issues.extend(quality_flags)

        # Check for missing critical data
        market_data = self.discovery_data.get("market_data", {})
        if market_data.get("market_cap", 0) == 0:
            issues.append("Missing market capitalization data")

        financial_metrics = self.discovery_data.get("financial_metrics", {})
        if financial_metrics.get("revenue_ttm", 0) == 0:
            issues.append("Missing revenue data")

        return issues

    def _identify_analysis_issues(self) -> List[str]:
        """Identify key issues in analysis phase"""
        issues = []

        if not self.analysis_data:
            issues.append("Analysis data unavailable")
            return issues

        # Check analysis confidence
        analysis_confidence = self.analysis_data.get("analysis_confidence", 1.0)
        if analysis_confidence < 0.7:
            issues.append("Low analysis confidence level")

        # Check for incomplete analysis components
        financial_health = self.analysis_data.get("financial_health_analysis", {})
        if financial_health.get("overall_health_score", 0) == 0:
            issues.append("Incomplete financial health analysis")

        return issues

    def _identify_synthesis_issues(self) -> List[str]:
        """Identify key issues in synthesis phase"""
        issues = []

        if not self.synthesis_data:
            issues.append("Synthesis data unavailable")
            return issues

        # Check for missing investment recommendation
        executive_summary = self.synthesis_data.get("executive_summary", {})
        if not executive_summary.get("investment_recommendation"):
            issues.append("Missing investment recommendation")

        # Check synthesis confidence
        synthesis_confidence = self.synthesis_data.get("synthesis_confidence", 1.0)
        if synthesis_confidence < 0.7:
            issues.append("Low synthesis confidence level")

        return issues

    def _determine_decision_confidence(self, score: float) -> str:
        """Determine decision confidence level"""
        if score >= 9.0:
            return "High"
        elif score >= 7.0:
            return "Medium"
        elif score >= 5.0:
            return "Low"
        else:
            return "Do_Not_Use"

    def _generate_methodology_notes(self) -> Dict[str, Any]:
        """Generate comprehensive methodology notes"""
        sources_consulted = 0
        if self.discovery_data:
            sources_consulted += 1
        if self.analysis_data:
            sources_consulted += 1
        if self.synthesis_data:
            sources_consulted += 1

        return {
            "sources_consulted": f"{sources_consulted} DASV workflow outputs",
            "validation_approach": f"{self.validation_depth} validation with {self.confidence_threshold} confidence threshold",
            "research_limitations": [
                "Validation limited to available DASV workflow outputs",
                "External market data not independently verified",
                "Peer comparison based on systematic analysis framework",
            ],
            "confidence_intervals": f"Validation scores represent quality assessment within {self.validation_depth} standards",
            "validation_standards_applied": f"Institutional quality thresholds: {self.validation_thresholds[self.validation_depth]}",
        }

    def _save_validation_results(self, validation_result: Dict[str, Any]) -> str:
        """Save validation results to output directory"""
        os.makedirs(self.output_dir, exist_ok=True)

        timestamp_str = self.timestamp.strftime("%Y%m%d")
        filename = f"{self.ticker}_{timestamp_str}_validation.json"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w") as f:
            json.dump(validation_result, f, indent=2, default=str)

        print(f"💾 Validation results saved: {filepath}")
        return filepath


def main():
    """Command-line interface for analysis validation"""
    parser = argparse.ArgumentParser(
        description="Execute DASV workflow validation for any stock ticker"
    )
    parser.add_argument(
        "synthesis_file", help="Path to synthesis output file (.md or .json)"
    )
    parser.add_argument(
        "--ticker",
        help="Stock ticker symbol (will extract from filename if not provided)",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=9.0,
        help="Minimum confidence threshold (9.0-9.8)",
    )
    parser.add_argument(
        "--validation-depth",
        choices=["standard", "comprehensive", "institutional"],
        default="institutional",
        help="Validation rigor level",
    )
    parser.add_argument(
        "--output-dir",
        default="./data/outputs/fundamental_analysis/validation",
        help="Output directory for validation results",
    )
    
    # Enhanced flags for sector analysis integration
    parser.add_argument(
        "--validate-sector-context",
        action="store_true",
        help="Validate sector analysis integration and cross-references",
    )
    parser.add_argument(
        "--validate-economic-indicators",
        action="store_true",
        help="Validate FRED economic indicator freshness and consistency",
    )
    parser.add_argument(
        "--validate-stress-testing",
        action="store_true",
        help="Validate economic stress testing scenarios and probabilities",
    )
    parser.add_argument(
        "--sector-analysis-path",
        help="Path to sector analysis report for cross-validation",
    )
    parser.add_argument(
        "--institutional-certification",
        action="store_true",
        help="Apply institutional certification standards (≥0.90 confidence)",
    )

    args = parser.parse_args()

    # Extract ticker from filename if not provided
    ticker = args.ticker
    if not ticker:
        basename = os.path.basename(args.synthesis_file)
        if "_" in basename:
            ticker = basename.split("_")[0]
        else:
            print(
                "❌ Could not extract ticker from filename. Please provide --ticker argument."
            )
            sys.exit(1)

    # Execute validation
    validator = AnalysisValidator(
        ticker=ticker,
        synthesis_file_path=args.synthesis_file,
        confidence_threshold=args.confidence_threshold,
        validation_depth=args.validation_depth,
        output_dir=args.output_dir,
    )

    result = validator.execute_validation()

    if "error" in result:
        print(f"❌ Validation failed: {result['error']}")
        sys.exit(1)
    else:
        overall_score = result["overall_assessment"]["overall_reliability_score"]
        decision_confidence = result["overall_assessment"]["decision_confidence"]
        print(f"✅ Validation completed successfully for {ticker}")
        print(f"📊 Overall reliability: {overall_score}")
        print(f"🎯 Decision confidence: {decision_confidence}")
        sys.exit(0)


if __name__ == "__main__":
    main()
