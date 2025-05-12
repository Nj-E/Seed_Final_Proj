import React from 'react';
import { likelihoodColors } from './utils';

interface DialPoint {
  label: string;
  angle: number;
}

interface InnerDialProps {
  center: number;
  centerY?: number;
  dialRadius: number;
  dialRotation: number;
  dialPoints: DialPoint[];
  dialIdx: number;
  likelihood: string;
  onDialPointClick: (index: number) => void;
  onHoverChange: (index: number | null) => void;
  hoverIdx: number | null;
}

export const InnerDial: React.FC<InnerDialProps> = ({
  center,
  centerY,
  dialRadius,
  dialRotation,
  dialPoints,
  dialIdx,
  likelihood,
  onDialPointClick,
  onHoverChange,
  hoverIdx
}) => {
  const cy = centerY ?? center;
  return (
    <g
      transform={`rotate(${dialRotation} ${center} ${cy})`}
      style={{ transition: 'transform 0.6s ease' }}
    >
      {dialPoints.map((point, idx) => {
        const angleRad = (point.angle * Math.PI) / 180 + Math.PI / 2;
        const x = center + dialRadius * Math.cos(angleRad);
        const y = cy + dialRadius * Math.sin(angleRad);
        const color = likelihoodColors[Object.values({probable: 'probable', plausible: 'plausible', possible: 'possible'})[idx]];
        const isHovered = hoverIdx === idx;
        const isSelected = idx === dialIdx;

        return (
          <g
            key={point.label}
            onMouseEnter={() => onHoverChange(idx)}
            onMouseLeave={() => onHoverChange(null)}
          >
            <circle
              cx={x}
              cy={y}
              r={isHovered ? 10 : 8}
              fill={color}
              stroke={isHovered || isSelected ? '#fff' : 'none'}
              strokeWidth={isHovered ? 2 : isSelected ? 1 : 0}
              onClick={() => onDialPointClick(idx)}
              style={{
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                filter: isHovered ? 'drop-shadow(0 0 4px rgba(255,255,255,0.4))' : 'none'
              }}
            />
            {(isHovered || isSelected) && (
              <text
                x={x}
                y={y - 18}
                textAnchor="middle"
                alignmentBaseline="middle"
                fontFamily="monospace"
                fontSize={12}
                fill="#fff"
                style={{
                  pointerEvents: 'none',
                  userSelect: 'none',
                  transition: 'transform 0.6s ease'
                }}
                transform={`rotate(${-dialRotation} ${x} ${y})`}
              >
                {point.label.toUpperCase()}
              </text>
            )}
          </g>
        );
      })}
    </g>
  );
};
