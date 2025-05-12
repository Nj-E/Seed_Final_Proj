import React, { useState, useEffect, useRef } from 'react';
import { SignalWheelProps, LikelihoodType, DragTypeValue } from './types';
import { describeArc, DIAL_POINTS, likelihoodColors, polarityColors, likelihoodToDegrees } from './utils';
import { OuterWheelSegments } from './OuterWheelSegments';
import { InnerDial } from './InnerDial';

export const WheelContainer: React.FC<SignalWheelProps & { heightScale?: number, svgClassName?: string, showTitle?: boolean, onFuturesConeChange?: (cone: string) => void }> = ({
  size = 40,
  polarity,
  likelihood,
  onChange = () => {},
  heightScale = 1.5,
  svgClassName = '',
  showTitle = false,
  onFuturesConeChange
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const center = size / 2;
  const outerRadius = center - 20;
  const innerRadius = 100;
  const [hoverIdx, setHoverIdx] = useState<number | null>(null);
  const [hoverSegment, setHoverSegment] = useState<number | null>(null);
  const [selectedCone, setSelectedCone] = useState<string | null>(null);
  const svgHeight = size * heightScale;
  const verticalCenter = svgHeight / 2;
  const labelOffset = outerRadius + 35;

  // Function to handle clicks on wheel segments
  const handleSegmentClick = (segmentIndex: number) => {
    const isRightSide = segmentIndex < 36 / 4 || segmentIndex >= 36 * 3 / 4;
    const newPolarity = isRightSide ? 'positive' : 'negative';
    if (polarity !== newPolarity) {
      onChange({ polarity: newPolarity, likelihood });
    }
  };

  const handleDialPointClick = (idx: number) => {
    const newLikelihood = Object.values(LikelihoodType)[idx];
    onChange({ polarity, likelihood: newLikelihood });
  };

  // Futures Cone filter handler
  const handleConeClick = (cone: string) => {
    setSelectedCone(cone);
    if (onFuturesConeChange) onFuturesConeChange(cone);
  };

  const dialIdxRaw = Object.values(LikelihoodType).indexOf(likelihood);
  const dialIdx = dialIdxRaw >= 0 ? dialIdxRaw : 0;
  const dialRotation = -DIAL_POINTS[dialIdx].angle;

  return (
    <div className="flex flex-col items-center">
      {showTitle && (
        <h2 className="text-white text-lg font-mono uppercase mb-2">Signal Wheel</h2>
      )}
      <div className="flex justify-center items-center py-12">
        <svg ref={svgRef} width={size} height={svgHeight} viewBox={`0 0 ${size} ${svgHeight}`} className={svgClassName}>
          {/* Background */}
          <circle 
            cx={center}
            cy={verticalCenter}
            r={outerRadius + 10}
            fill="black"
          />
          {/* Outer wheel segments */}
          <OuterWheelSegments 
            center={center}
            centerY={verticalCenter}
            outerRadius={outerRadius}
            segmentCount={36}
            polarity={polarity}
            onSegmentClick={handleSegmentClick}
            onHoverChange={setHoverSegment}
            hoverSegment={hoverSegment}
          /> 
          {/* Inner circles */}
          <circle
            cx={center}
            cy={verticalCenter}
            r={innerRadius}
            fill="#111726"
            stroke="#293E6B"
            strokeWidth={1}
          />
          <circle
            cx={center}
            cy={verticalCenter}
            r={innerRadius - 15}
            fill="#0F1420"
            stroke="#293E6B"
            strokeWidth={1}
          />
          <text
            key={likelihood}
            x={center}
            y={verticalCenter}
            fill="#fff"
            fontSize={14}
            fontFamily="monospace"
            textAnchor="middle"
            dominantBaseline="middle"
            style={{
              fontWeight: 'bold',
              letterSpacing: 1,
              opacity: 1,
              textTransform: 'uppercase',
              transition: 'opacity 0.4s'
            }}
          >
            {typeof likelihood === 'string' && likelihood
              ? likelihood
              : 'SELECT'}
          </text>
          {/* Inner Dial */}
          <InnerDial 
            center={center} 
            centerY={verticalCenter}
            dialRadius={innerRadius + 30}
            dialRotation={dialRotation}
            dialPoints={DIAL_POINTS}
            dialIdx={dialIdx}
            likelihood={likelihood}
            onDialPointClick={handleDialPointClick}
            onHoverChange={setHoverIdx}
            hoverIdx={hoverIdx}
          />
        </svg>
      </div>
    </div>
  );
};
