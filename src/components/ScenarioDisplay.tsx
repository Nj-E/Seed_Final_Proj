/**
 * ScenarioDisplay.tsx
 * Displays a scenario and its contributing signals in the SEED platform.
 * Author: [Your Name]
 * Date: [YYYY-MM-DD]
 */

import React from 'react';
import { Scenario, Signal } from '../types/seed';
import { Badge } from "@/components/ui/badge"; 

interface ScenarioDisplayProps {
  scenario: Scenario | null;
  signals: Signal[];
}

/**
 * ScenarioDisplay
 * Shows scenario details and lists contributing signals.
 * If no scenario is selected, shows a placeholder message.
 */
const ScenarioDisplay: React.FC<ScenarioDisplayProps> = ({ scenario, signals }) => {
  if (!scenario) {
    // Show placeholder if no scenario is selected
    return (
      <div className="h-full flex items-center justify-center border border-dashed border-gray-700 rounded-lg p-6">
        <p className="text-gray-500 text-sm">No scenario selected</p>
      </div>
    );
  }
 

  return (
    <div className="bg-seed-darkgray/30 border border-seed-lightgray/20 rounded-lg p-5 animate-fade-in">
      <div className="flex items-center mb-3">
        {/* Show scenario polarity and likelihood as badges */}
        <Badge 
          className={`mr-2 ${scenario.polarity === 'positive' ? 'bg-green-500 text-black' : scenario.polarity === 'negative' ? 'bg-red-500 text-white' : 'bg-gray-400 text-black'}`}
        >
          {scenario.polarity.toUpperCase()}
        </Badge>
        <Badge className={`text-white`} style={{ backgroundColor: '#293E6B' }}>
          {scenario.likelihood.toUpperCase()}
        </Badge>
      </div>
      <h2 className="text-xl font-bold mb-2">{scenario.title}</h2>
      <div className="mb-2 text-gray-300"><strong>Description:</strong> {scenario.description}</div>
      {scenario && scenario.sources && scenario.sources.length > 0 && (
        <div className="mt-4">
          <h3 className="font-semibold mb-1">Sources:</h3>
          <ul className="list-disc list-inside text-xs text-gray-400">
            {scenario.sources.map((src, idx) => (
              <li key={idx}>{src}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ScenarioDisplay;
