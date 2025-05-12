import React from 'react';
import { describeArc, polarityColors } from './utils';
import { Polarity } from './types';

interface OuterWheelSegmentsProps {
  center: number;
  centerY?: number;
  outerRadius: number;
  segmentCount: number;
  polarity: Polarity;
  onSegmentClick: (index: number) => void;
  onHoverChange: (index: number | null) => void;
  hoverSegment: number | null;
}

export const OuterWheelSegments: React.FC<OuterWheelSegmentsProps> = ({
  center,
  centerY,
  outerRadius,
  segmentCount,
  polarity,
  onSegmentClick,
  onHoverChange,
  hoverSegment
}) => {
  const cy = centerY ?? center;
  const segments = Array.from({ length: segmentCount }, (_, i) => {
    const start = i * (360 / segmentCount) + 0.5;
    const end = (i + 1) * (360 / segmentCount) - 0.5;

    const isPositiveSide = i < segmentCount / 4 || i >= segmentCount * 3 / 4;
    const isActive = polarity === 'positive' ? isPositiveSide : !isPositiveSide;
    const color = isPositiveSide ? polarityColors['positive'] : polarityColors['negative'];
    const isHovered = hoverSegment === i;

    return (
      <path
        key={i}
        d={describeArc(center, cy, outerRadius, start, end)}
        stroke={isActive || isHovered ? color : '#444'}
        strokeWidth={isHovered ? 30 : 20}
        strokeDasharray="4 4"
        fill="none"
        onMouseEnter={() => onHoverChange(i)}
        onMouseLeave={() => onHoverChange(null)}
        onClick={() => onSegmentClick(i)}
        style={{
          cursor: 'pointer',
          opacity: isActive ? 0.9 : isHovered ? 0.7 : 0.2,
          transition: 'opacity 0.2s, stroke-width 0.2s'
        }}
      />
    );
  });

  return (
    <>
      {/* Outer arc segments */}
      <g>{segments}</g>
      {/* Top label */}
      <text
        x={center}
        y={cy - outerRadius - 30}
        fill="#ccc"
        fontFamily="monospace"
        fontSize={14}
        textAnchor="middle"
      >
        Positive
      </text>

      {/* Bottom label */}
      <text
        x={center}
        y={cy + outerRadius + 30}
        fill="#ccc"
        fontFamily="monospace"
        fontSize={14}
        textAnchor="middle"
      >
        Negative
      </text>
    </>
  );
};
