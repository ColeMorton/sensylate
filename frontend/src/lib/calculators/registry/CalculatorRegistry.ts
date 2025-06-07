import type { BaseCalculator, CalculatorMetadata } from "../core/Calculator.ts";
import { PocketCalculator } from "../implementations/PocketCalculator.ts";
import { MortgageCalculator } from "../implementations/MortgageCalculator.ts";
import { DCACalculator } from "../implementations/DCACalculator.ts";

export interface CalculatorRegistryEntry {
  metadata: CalculatorMetadata;
  calculator: () => BaseCalculator;
  loaded?: boolean;
}

export class CalculatorRegistry {
  private static instance: CalculatorRegistry;
  private calculators = new Map<string, CalculatorRegistryEntry>();
  private categories = new Map<string, string[]>();

  private constructor() {
    this.registerBuiltInCalculators();
  }

  static getInstance(): CalculatorRegistry {
    if (!CalculatorRegistry.instance) {
      CalculatorRegistry.instance = new CalculatorRegistry();
    }
    return CalculatorRegistry.instance;
  }

  private registerBuiltInCalculators(): void {
    this.register("pocket-calculator", {
      metadata: new PocketCalculator().metadata,
      calculator: () => new PocketCalculator(),
    });

    this.register("mortgage-calculator", {
      metadata: new MortgageCalculator().metadata,
      calculator: () => new MortgageCalculator(),
    });

    this.register("dca-calculator", {
      metadata: new DCACalculator().metadata,
      calculator: () => new DCACalculator(),
    });
  }

  register(id: string, entry: Omit<CalculatorRegistryEntry, "loaded">): void {
    this.calculators.set(id, { ...entry, loaded: false });

    // Update category index
    const category = entry.metadata.category;
    if (!this.categories.has(category)) {
      this.categories.set(category, []);
    }
    const categoryCalculators = this.categories.get(category)!;
    if (!categoryCalculators.includes(id)) {
      categoryCalculators.push(id);
    }
  }

  unregister(id: string): boolean {
    const entry = this.calculators.get(id);
    if (!entry) {
      return false;
    }

    // Remove from category index
    const category = entry.metadata.category;
    const categoryCalculators = this.categories.get(category);
    if (categoryCalculators) {
      const index = categoryCalculators.indexOf(id);
      if (index > -1) {
        categoryCalculators.splice(index, 1);
        if (categoryCalculators.length === 0) {
          this.categories.delete(category);
        }
      }
    }

    return this.calculators.delete(id);
  }

  get(id: string): BaseCalculator | null {
    const entry = this.calculators.get(id);
    if (!entry) {
      return null;
    }

    try {
      const calculator = entry.calculator();
      entry.loaded = true;
      return calculator;
    } catch {
      // Failed to load calculator
      return null;
    }
  }

  getMetadata(id: string): CalculatorMetadata | null {
    const entry = this.calculators.get(id);
    return entry ? entry.metadata : null;
  }

  list(): CalculatorMetadata[] {
    return Array.from(this.calculators.values()).map((entry) => entry.metadata);
  }

  listByCategory(category: string): CalculatorMetadata[] {
    const calculatorIds = this.categories.get(category) || [];
    return calculatorIds
      .map((id) => this.calculators.get(id)?.metadata)
      .filter(
        (metadata): metadata is CalculatorMetadata => metadata !== undefined,
      );
  }

  getCategories(): string[] {
    return Array.from(this.categories.keys()).sort();
  }

  search(query: string): CalculatorMetadata[] {
    const searchTerm = query.toLowerCase();
    return this.list().filter(
      (metadata) =>
        metadata.name.toLowerCase().includes(searchTerm) ||
        metadata.description.toLowerCase().includes(searchTerm) ||
        metadata.category.toLowerCase().includes(searchTerm) ||
        metadata.tags?.some((tag) => tag.toLowerCase().includes(searchTerm)),
    );
  }

  exists(id: string): boolean {
    return this.calculators.has(id);
  }

  isLoaded(id: string): boolean {
    const entry = this.calculators.get(id);
    return entry?.loaded ?? false;
  }

  getStats(): {
    total: number;
    loaded: number;
    categories: number;
    byCategory: Record<string, number>;
  } {
    const entries = Array.from(this.calculators.values());
    const byCategory: Record<string, number> = {};

    entries.forEach((entry) => {
      const category = entry.metadata.category;
      byCategory[category] = (byCategory[category] || 0) + 1;
    });

    return {
      total: entries.length,
      loaded: entries.filter((entry) => entry.loaded).length,
      categories: this.categories.size,
      byCategory,
    };
  }
}

// Singleton instance
export const calculatorRegistry = CalculatorRegistry.getInstance();
