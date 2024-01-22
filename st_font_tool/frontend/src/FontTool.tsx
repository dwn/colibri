import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import FontToolUtil from "./FontToolUtil.js"
import './FontTool.css'
interface State {
  isFocused: boolean
}
class FontTool extends StreamlitComponentBase<State> {
  public state = { isFocused: false }
  fontCanvasRef = React.createRef<HTMLCanvasElement>();
  ctx: CanvasRenderingContext2D | null | undefined = null;
  /////////////////////////////////////////////
  componentDidUpdate() {
    this.ctx = this.fontCanvasRef?.current?.getContext('2d');
    if (this.ctx) FontToolUtil.drawImageAndGetSVG(this.ctx, this.props.args["fontGlyphCode"]);
  }
  /////////////////////////////////////////////
  public render = (): ReactNode => {
    const { theme } = this.props
    const fontCanvasStyle: React.CSSProperties = {}
    fontCanvasStyle.backgroundImage = "url(data:image/svg+xml;base64," + btoa(FontToolUtil.constant.svgStrGrid) + ")";
    if (theme) {
      fontCanvasStyle.backgroundColor = this.state.isFocused ?
        theme.secondaryBackgroundColor : theme.backgroundColor;
    }
    return (
      <div>
        <canvas id='font-canvas' width='500' height='500' onMouseEnter={this.onMouseEnter} onMouseLeave={this.onMouseLeave} style={fontCanvasStyle} ref={this.fontCanvasRef}/>
        <canvas id='scratch-canvas' width='500' height='500'/>
        <img id="scratch-img" alt="scratch image"/>
      </div>
    )
  }
  private onMouseEnter = (): void => {
    this.setState({ isFocused: true })
  }
  private onMouseLeave = (): void => {
    this.setState({ isFocused: false })
  }
}
export default withStreamlitConnection(FontTool)
