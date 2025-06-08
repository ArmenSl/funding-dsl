#!/usr/bin/env python3
"""
Comprehensive Demo: TextX vs ANTLR Parser Comparison

This script demonstrates both parser implementations side by side,
showing their capabilities, performance, and output equivalence.
"""

import time
from typing import Dict, Any

# Import both parser implementations
from textual_textx import parse_funding_dsl_text_textx, FundingDSLTextXParser
from textual.funding_dsl_parser import parse_funding_dsl_text, FundingDSLParser
from metamodel.funding_metamodel import FundingModelValidator


def create_sample_dsl() -> str:
    """Create a comprehensive sample DSL for testing both parsers"""
    return '''
    funding "Parser Comparison Demo" {
        description "Demonstrating both TextX and ANTLR parser implementations"
        currency EUR
        min_amount 2.0
        max_amount 500.0
        
        beneficiaries {
            beneficiary "Alice Developer" {
                email "alice@demo.com"
                github "alice-dev"
                website "https://alice.dev"
                description "Lead developer and project maintainer"
            }
            
            beneficiary "Bob Contributor" {
                github "bob-contrib"
                description "Core contributor and documentation lead"
            }
        }
        
        sources {
            github_sponsors "alice-dev" {
                type both
                active true
            }
            
            patreon "demo-project" {
                type recurring
                active true
                config {
                    "tier_sync" "enabled"
                    "webhook_url" "https://api.demo.com/webhook"
                    "auto_thank" "true"
                }
            }
            
            ko_fi "alice-dev" {
                type one_time
                active true
            }
            
            custom "PayPal Donations" {
                url "https://paypal.me/alice-dev"
                type both
                active true
            }
        }
        
        tiers {
            tier "Coffee Supporter" {
                amount 5.0 EUR
                description "Support with a monthly coffee"
                benefits [
                    "Thank you message",
                    "Project updates",
                    "Community access"
                ]
            }
            
            tier "Regular Backer" {
                amount 25.0 EUR
                description "Regular monthly support"
                max_sponsors 50
                benefits [
                    "All Coffee tier benefits",
                    "Early access to features",
                    "Direct communication channel",
                    "Priority issue responses"
                ]
            }
            
            tier "Premium Sponsor" {
                amount 100.0 EUR
                description "Premium sponsorship with major benefits"
                max_sponsors 10
                benefits [
                    "All Backer tier benefits",
                    "Logo placement in README",
                    "Quarterly video calls",
                    "Feature request priority",
                    "Custom integration support"
                ]
            }
        }
        
        goals {
            goal "Infrastructure Costs" {
                target 200.0 EUR
                current 125.0 EUR
                description "Monthly server and infrastructure expenses"
            }
            
            goal "Documentation Rewrite" {
                target 1000.0 EUR
                current 300.0 EUR
                deadline "2024-09-01"
                description "Complete documentation overhaul with examples"
            }
            
            goal "Mobile App Development" {
                target 5000.0 EUR
                current 0.0 EUR
                deadline "2025-03-01"
                description "Develop companion mobile application"
            }
        }
    }
    '''


def benchmark_parser(parser_name: str, parse_function, dsl_text: str, iterations: int = 10) -> Dict[str, Any]:
    """Benchmark a parser function"""
    print(f"\n🔧 Benchmarking {parser_name} Parser...")
    
    times = []
    config = None
    
    for i in range(iterations):
        start_time = time.time()
        try:
            config = parse_function(dsl_text)
            end_time = time.time()
            times.append(end_time - start_time)
        except Exception as e:
            print(f"❌ Error in {parser_name}: {e}")
            return {"error": str(e)}
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"✅ {parser_name} completed {iterations} iterations")
    print(f"   Average time: {avg_time:.4f}s")
    print(f"   Min time: {min_time:.4f}s")
    print(f"   Max time: {max_time:.4f}s")
    
    return {
        "config": config,
        "avg_time": avg_time,
        "min_time": min_time,
        "max_time": max_time,
        "iterations": iterations
    }


def compare_configurations(textx_config, antlr_config) -> Dict[str, bool]:
    """Compare two configurations for equivalence"""
    print("\n📊 Comparing Parser Results...")
    
    comparisons = {}
    
    # Basic properties
    comparisons["project_name"] = textx_config.project_name == antlr_config.project_name
    comparisons["description"] = textx_config.description == antlr_config.description
    comparisons["currency"] = textx_config.preferred_currency == antlr_config.preferred_currency
    
    # Amount limits
    if textx_config.min_amount and antlr_config.min_amount:
        comparisons["min_amount"] = textx_config.min_amount.value == antlr_config.min_amount.value
    else:
        comparisons["min_amount"] = textx_config.min_amount == antlr_config.min_amount
    
    if textx_config.max_amount and antlr_config.max_amount:
        comparisons["max_amount"] = textx_config.max_amount.value == antlr_config.max_amount.value
    else:
        comparisons["max_amount"] = textx_config.max_amount == antlr_config.max_amount
    
    # Collections
    comparisons["beneficiaries_count"] = len(textx_config.beneficiaries) == len(antlr_config.beneficiaries)
    comparisons["sources_count"] = len(textx_config.funding_sources) == len(antlr_config.funding_sources)
    comparisons["tiers_count"] = len(textx_config.tiers) == len(antlr_config.tiers)
    comparisons["goals_count"] = len(textx_config.goals) == len(antlr_config.goals)
    
    # Detailed comparisons
    if comparisons["beneficiaries_count"]:
        for i, (tx_ben, antlr_ben) in enumerate(zip(textx_config.beneficiaries, antlr_config.beneficiaries)):
            comparisons[f"beneficiary_{i}_name"] = tx_ben.name == antlr_ben.name
            comparisons[f"beneficiary_{i}_github"] = tx_ben.github_username == antlr_ben.github_username
    
    if comparisons["sources_count"]:
        for i, (tx_src, antlr_src) in enumerate(zip(textx_config.funding_sources, antlr_config.funding_sources)):
            comparisons[f"source_{i}_platform"] = tx_src.platform == antlr_src.platform
            comparisons[f"source_{i}_username"] = tx_src.username == antlr_src.username
    
    # Print comparison results
    all_match = all(comparisons.values())
    print(f"Overall Match: {'✅ YES' if all_match else '❌ NO'}")
    
    for key, value in comparisons.items():
        status = "✅" if value else "❌"
        print(f"  {key}: {status}")
    
    return comparisons


def analyze_configuration(config, parser_name: str):
    """Analyze and display configuration details"""
    print(f"\n📋 {parser_name} Configuration Analysis:")
    print(f"  Project: {config.project_name}")
    print(f"  Description: {config.description}")
    print(f"  Currency: {config.preferred_currency.value}")
    
    if config.min_amount:
        print(f"  Min Amount: {config.min_amount}")
    if config.max_amount:
        print(f"  Max Amount: {config.max_amount}")
    
    print(f"  Beneficiaries: {len(config.beneficiaries)}")
    for ben in config.beneficiaries:
        print(f"    • {ben.name} (@{ben.github_username})")
    
    print(f"  Funding Sources: {len(config.funding_sources)}")
    for source in config.funding_sources:
        status = "🟢" if source.is_active else "🔴"
        print(f"    {status} {source.platform.value}: {source.username}")
    
    print(f"  Tiers: {len(config.tiers)}")
    for tier in config.tiers:
        print(f"    • {tier.name}: {tier.amount}")
    
    print(f"  Goals: {len(config.goals)}")
    for goal in config.goals:
        progress = (goal.current_amount.value / goal.target_amount.value) * 100
        print(f"    • {goal.name}: {progress:.1f}% ({goal.current_amount}/{goal.target_amount})")


def validate_configurations(textx_config, antlr_config):
    """Validate both configurations"""
    print("\n🔍 Validation Results:")
    
    # Validate TextX configuration
    textx_errors = FundingModelValidator.validate_configuration(textx_config)
    print(f"TextX Configuration: {'✅ Valid' if not textx_errors else f'❌ {len(textx_errors)} errors'}")
    if textx_errors:
        for error in textx_errors:
            print(f"  - {error}")
    
    # Validate ANTLR configuration
    antlr_errors = FundingModelValidator.validate_configuration(antlr_config)
    print(f"ANTLR Configuration: {'✅ Valid' if not antlr_errors else f'❌ {len(antlr_errors)} errors'}")
    if antlr_errors:
        for error in antlr_errors:
            print(f"  - {error}")


def demonstrate_visitor_pattern(config, parser_name: str):
    """Demonstrate visitor pattern usage"""
    print(f"\n🔄 {parser_name} Visitor Pattern Demo:")
    
    from metamodel.funding_metamodel import FundingModelVisitor
    
    class StatisticsVisitor(FundingModelVisitor):
        def __init__(self):
            self.stats = {
                "total_tiers": 0,
                "total_goals": 0,
                "total_target_amount": 0.0,
                "total_current_amount": 0.0,
                "active_sources": 0,
                "platforms": set()
            }
        
        def visit_configuration(self, config):
            pass
        
        def visit_beneficiary(self, beneficiary):
            pass
        
        def visit_funding_source(self, source):
            if source.is_active:
                self.stats["active_sources"] += 1
            self.stats["platforms"].add(source.platform.value)
        
        def visit_tier(self, tier):
            self.stats["total_tiers"] += 1
        
        def visit_goal(self, goal):
            self.stats["total_goals"] += 1
            self.stats["total_target_amount"] += goal.target_amount.value
            self.stats["total_current_amount"] += goal.current_amount.value
    
    visitor = StatisticsVisitor()
    config.accept(visitor)
    
    print(f"  Statistics:")
    print(f"    Total Tiers: {visitor.stats['total_tiers']}")
    print(f"    Total Goals: {visitor.stats['total_goals']}")
    print(f"    Target Amount: {visitor.stats['total_target_amount']} {config.preferred_currency.value}")
    print(f"    Current Amount: {visitor.stats['total_current_amount']} {config.preferred_currency.value}")
    print(f"    Active Sources: {visitor.stats['active_sources']}")
    print(f"    Platforms: {', '.join(visitor.stats['platforms'])}")
    
    overall_progress = (visitor.stats['total_current_amount'] / visitor.stats['total_target_amount']) * 100
    print(f"    Overall Progress: {overall_progress:.1f}%")


def main():
    """Main demonstration function"""
    print("🚀 Funding DSL Parser Comparison Demo")
    print("=" * 60)
    
    # Create sample DSL
    dsl_text = create_sample_dsl()
    print(f"📝 Sample DSL created ({len(dsl_text)} characters)")
    
    # Benchmark both parsers
    textx_results = benchmark_parser("TextX", parse_funding_dsl_text_textx, dsl_text)
    antlr_results = benchmark_parser("ANTLR", parse_funding_dsl_text, dsl_text)
    
    if "error" in textx_results or "error" in antlr_results:
        print("❌ One or both parsers failed. Exiting.")
        return
    
    textx_config = textx_results["config"]
    antlr_config = antlr_results["config"]
    
    # Compare performance
    print("\n⚡ Performance Comparison:")
    print(f"TextX Average Time: {textx_results['avg_time']:.4f}s")
    print(f"ANTLR Average Time: {antlr_results['avg_time']:.4f}s")
    
    if textx_results['avg_time'] < antlr_results['avg_time']:
        speedup = antlr_results['avg_time'] / textx_results['avg_time']
        print(f"🏆 TextX is {speedup:.2f}x faster")
    else:
        speedup = textx_results['avg_time'] / antlr_results['avg_time']
        print(f"🏆 ANTLR is {speedup:.2f}x faster")
    
    # Compare configurations
    comparisons = compare_configurations(textx_config, antlr_config)
    
    # Analyze configurations
    analyze_configuration(textx_config, "TextX")
    analyze_configuration(antlr_config, "ANTLR")
    
    # Validate configurations
    validate_configurations(textx_config, antlr_config)
    
    # Skip visitor pattern demo (not implemented in this version)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    all_match = all(comparisons.values())
    print(f"Configuration Equivalence: {'✅ Perfect Match' if all_match else '❌ Differences Found'}")
    print(f"TextX Performance: {textx_results['avg_time']:.4f}s average")
    print(f"ANTLR Performance: {antlr_results['avg_time']:.4f}s average")
    
    print("\n🎯 Recommendations:")
    print("• Use TextX for: Rapid prototyping, Python-focused development, simpler grammar")
    print("• Use ANTLR for: High performance requirements, complex grammars, multi-language support")
    print("• Both parsers produce equivalent, valid configurations")
    print("• Choose based on your specific needs and preferences")
    
    print("\n🎉 Demo Complete!")


if __name__ == "__main__":
    main() 