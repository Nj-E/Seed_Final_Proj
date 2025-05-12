export type Polarity = 'positive' | 'negative';
export type Likelihood = 'probable' | 'plausible' | 'possible';

export interface Signal {
  id: string;
  title: string;
  description: string;
  source: string;
  source_pdf?: string;
  page?: number;
  text?: string;
}

export interface Scenario {
  id: string;
  title: string;
  description: string;
  polarity: Polarity;
  likelihood: Likelihood;
  likelihoodValue: number;
  timeframe: number; // in years
  contributingSignals: string[]; // Signal IDs
  sources?: string[];
}
