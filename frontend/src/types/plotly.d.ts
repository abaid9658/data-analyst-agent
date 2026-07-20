// Type declarations for plotly.js-dist-min (no @types package available)
declare module 'plotly.js-dist-min' {
  interface PlotlyHTMLElement extends HTMLElement {
    data: PlotlyData[];
    layout: Partial<PlotlyLayout>;
    _fullLayout: PlotlyLayout;
  }

  type PlotlyData = any;
  type PlotlyLayout = any;
  type PlotlyConfig = any;

  function newPlot(
    root: HTMLElement | string,
    data: PlotlyData[],
    layout?: Partial<PlotlyLayout>,
    config?: Partial<PlotlyConfig>
  ): Promise<PlotlyHTMLElement>;

  function react(
    root: HTMLElement | string,
    data: PlotlyData[],
    layout?: Partial<PlotlyLayout>,
    config?: Partial<PlotlyConfig>
  ): Promise<PlotlyHTMLElement>;

  function purge(root: HTMLElement | string): void;

  function toImage(
    root: HTMLElement | string,
    opts?: { format?: string; width?: number; height?: number; scale?: number }
  ): Promise<string>;

  function downloadImage(
    root: HTMLElement | string,
    opts?: { format?: string; filename?: string; width?: number; height?: number }
  ): Promise<string>;
}
