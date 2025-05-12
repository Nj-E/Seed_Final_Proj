export type Polarity = 'positive' | 'negative';
export type Likelihood = 'probable' | 'plausible' | 'possible';

export const LikelihoodType = {
  PROBABLE: 'probable',
  PLAUSIBLE: 'plausible',
  POSSIBLE: 'possible'
} as const;

export type DragTypeValue = 'polarity' | 'likelihood' | 'none';

export interface SignalWheelProps {
  size?: number;
  polarity: Polarity;
  likelihood: Likelihood;
  onChange?: (update: {
    polarity: Polarity;
    likelihood: Likelihood;
  }) => void;
}
