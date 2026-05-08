declare module 'react-katex' {
  import type React from 'react';

  export function InlineMath(props: { math: string; errorColor?: string; renderError?: (error: Error) => React.ReactNode }): JSX.Element;
  export function BlockMath(props: { math: string; errorColor?: string; renderError?: (error: Error) => React.ReactNode }): JSX.Element;
}
