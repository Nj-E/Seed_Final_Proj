/**
 * Index.tsx
 * Main page for SEED: Speculative Futures Platform.
 * Handles state, data fetching, scenario/signal filtering, and main UI logic.
 * Author: [Your Name]
 * Date: [YYYY-MM-DD]
 */

import React, { useState, useEffect } from 'react';
import { Separator } from '@/components/ui/separator';
import SignalWheel from '@/components/SignalWheel';
import ScenarioDisplay from '@/components/ScenarioDisplay';
import SignalList from '@/components/SignalList';
import { Scenario, Signal, Polarity, Likelihood } from '@/types/seed';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { FaSpinner } from 'react-icons/fa';

const Index = () => {
  // Toast for user feedback
  const { toast } = useToast();
  // State for user selection and data
  const [polarity, setPolarity] = useState<Polarity>('positive');
  const [likelihood, setLikelihood] = useState<Likelihood>('plausible');
  const [signals, setSignals] = useState<Signal[]>([]);
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [currentScenario, setCurrentScenario] = useState<Scenario | null>(null);
  const [buttonState, setButtonState] = useState<'default' | 'loading' | 'success'>('default');
  
  /**
   * Fetch signals and scenarios from FastAPI backend on mount.
   * This keeps the app data-driven and easy to update.
   */
  useEffect(() => {
    const fetchData = async () => {
      const [signalsRes, scenariosRes] = await Promise.all([
        fetch('/data/signals.json'),
        fetch('/data/scenarios.json'),
      ]);
      const signalsData = await signalsRes.json();
      const scenariosData = await scenariosRes.json();
      setSignals(signalsData);
      setScenarios(scenariosData);
      // Do not set currentScenario here; user must generate one
    };
    fetchData();
  }, []);
  
  /**
   * When the user changes the wheel, clear the current scenario to hide content
   * This ensures the scenario always matches the current selection
   */
  const handleSignalWheelChange = (update: {
    polarity: Polarity;
    likelihood: Likelihood;
  }) => {
    setPolarity(update.polarity);
    setLikelihood(update.likelihood);
    setCurrentScenario(null);
  };
  
  /**
   * Filters scenarios based on current polarity and likelihood.
   * Returns only scenarios matching the user's selection.
   */
  const filteredScenarios = scenarios.filter(
    (scn) => scn.polarity === polarity && scn.likelihood === likelihood
  );
  
  /**
   * Only show signals for the current scenario.
   * This keeps the UI focused and relevant.
   */
  const relevantSignalIds = new Set(currentScenario ? currentScenario.contributingSignals : []);
  const filteredSignals = signals.filter((sig) => relevantSignalIds.has(sig.id));
  
  console.log('filteredSignals', filteredSignals);
  
  /**
   * When the user clicks Generate/Regenerate Scenario, show loading, then success, then reset.
   */
  const handleGenerateScenario = () => {
    if (filteredScenarios.length === 0) {
      setCurrentScenario(null);
      toast({ title: "No scenario found", description: "No scenario matches your selection.", duration: 3000 });
      return;
    }
    setButtonState('loading');
    setTimeout(() => {
      const randomIdx = Math.floor(Math.random() * filteredScenarios.length);
      setCurrentScenario(filteredScenarios[randomIdx]);
      setButtonState('success');
      setTimeout(() => setButtonState('default'), 900); // Show success for 0.9s
    }, 700); // Simulate loading for 0.7s
  };
  
  /**
   * Handles editing and deleting signals (UI feedback only; not persisted)
   */
  const handleEditSignal = (id: string) => {
    toast({
      title: "Edit Signal",
      description: `Editing signal: ${id}`,
      duration: 3000,
    });
  };
  const handleDeleteSignal = (id: string) => {
    toast({
      title: "Delete Signal",
      description: `Deleting signal: ${id}`,
      duration: 3000,
    });
    setSignals(signals.filter(signal => signal.id !== id));
  };

  // --- UI Rendering ---
  return (
    <div className="flex flex-col min-h-screen p-4 md:p-6 max-w-screen-2xl mx-auto">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center">
          <div className="h-3 w-3 bg-seed-positive rounded-full mr-2"></div>
          <h1 className="text-lg font-mono font-bold">SEED</h1>
          <span className="text-xs text-gray-500 ml-2">SPECULATIVE DESIGN PLATFORM</span>
        </div>
      </div>
      
      {/* Main Content */}
      <div className="flex flex-col md:flex-row gap-6">
        {/* Left Column: Signal Wheel only */}
        <div className="w-full md:w-1/2">
          <div className="bg-seed-darkgray/50 border border-seed-lightgray/20 rounded-lg  flex justify-center">
            <SignalWheel
              polarity={polarity}
              likelihood={likelihood}
              onChange={handleSignalWheelChange}
            />
          </div>
        </div>
        {/* Right Column: Generate button, Scenario and Signal List */}
        <div className="w-full md:w-1/2 flex flex-col items-center">
          <div className="w-full flex justify-end mb-4">
            <Button
              className={`border border-white bg-seed-darkgray/90 text-white text-xs h-8 transition-all duration-300
                ${buttonState === 'loading' ? 'animate-pulse opacity-80' : ''}
                ${buttonState === 'success' ? 'bg-green-500 border-green-500 text-black animate-fade' : ''}`}
              onClick={handleGenerateScenario}
              disabled={buttonState === 'loading'}
            >
              {buttonState === 'loading' && (
                <FaSpinner className="mr-2 animate-spin inline-block" />
              )}
              {buttonState === 'success'
                ? 'Scenario Ready!'
                : currentScenario
                  ? 'Regenerate Scenario'
                  : 'Generate Scenario'}
            </Button>
          </div>
          {/* Show scenario and signals if one is selected, otherwise show placeholder */}
          {currentScenario ? (
            <>
              <div className="w-full">
                <ScenarioDisplay scenario={currentScenario} signals={filteredSignals} />
                {/* Styled signals list matching SignalList, but for scenario signals */}
                <div className="bg-seed-darkgray/50 rounded-lg p-4 w-full mt-4">
                  <h2 className="text-sm font-mono font-bold mb-4">Signals Used</h2>
                  <div className="space-y-3">
                    {filteredSignals.map((sig) => (
                      <div key={sig.id} className="signal-card">
                        <div className="flex justify-between">
                          <h3 className="font-medium">{sig.title || sig.id}</h3>
                        </div>
                        <p className="text-gray-400 text-xs mb-2">
                          {sig.text ? (sig.text.length > 200 ? sig.text.slice(0, 200) + '...' : sig.text) : sig.description}
                        </p>
                        <div className="flex justify-between text-xs">
                          <span className="text-gray-500">
                            Source: {sig.source_pdf ? `${sig.source_pdf}` : sig.source}{sig.page ? `, p.${sig.page}` : ''}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
             </>
          ) : (
            <div className="w-full flex flex-col items-center justify-center py-12 text-gray-400">
              <div className="text-lg font-mono mb-2">No scenario selected</div>
              <div className="text-sm">Select a polarity and likelihood, then click <span className='font-bold'>Generate Scenario</span>.</div>
            </div>
          )}
        </div>
      </div>
      {/* Bottom Status Bar */}
      <div className="mt-auto pt-4">
        <Separator className="mb-4" />
        <div className="flex justify-between text-xs text-gray-500">
          <div>SEED v0.1 - SPECULATIVE FUTURES</div>
          <div className="flex space-x-4">
            <span>{new Date().getFullYear()} DESIGN FUTURES LAB</span>
            <span>SIGNALS: {filteredSignals.length}</span>
            <span>SCENARIOS: {filteredScenarios.length}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
