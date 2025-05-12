import React from 'react';
import { SignalWheelProps } from './types';
import { WheelContainer } from './WheelContainer';

const SignalWheel: React.FC<SignalWheelProps> = ({
  size = 400,
  polarity,
  likelihood,
  onChange = () => {}
}) => {
  return (
    <WheelContainer 
      size={size}
      polarity={polarity}
      likelihood={likelihood}
      onChange={onChange}
    />
  );
};

export default SignalWheel;
