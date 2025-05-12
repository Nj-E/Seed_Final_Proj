import React from 'react';
import { Signal } from '../types/seed';
import { Button } from "@/components/ui/button";

interface SignalListProps {
  signals: Signal[];
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  polarity?: string;
  likelihood?: string;
}

const SignalList: React.FC<SignalListProps> = ({ signals, onEdit, onDelete, polarity, likelihood }) => {
  return (
    <div className="bg-seed-darkgray/50   rounded-lg p-4 w-full  ">
      <h2 className="text-sm font-mono font-bold mb-4">Signals</h2>
      
      <div className="space-y-3">
        {signals.map(signal => (
          <div key={signal.id} className="signal-card">
            <div className="flex justify-between">
              <h3 className="font-medium">{signal.title}</h3>
            </div>
            <p className="text-gray-400 text-xs mb-2">{signal.description}</p>
            <div className="flex justify-between text-xs">
              <span className="text-gray-500">Source: {signal.source}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SignalList;
