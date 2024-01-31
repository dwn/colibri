import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from 'streamlit-component-lib'
import React, { ReactNode } from 'react'
import FontToolUtil from './FontToolUtil.js'
import './style.css'
interface State {
  isFocused: boolean
}
class FontTool extends StreamlitComponentBase<State> {
  public state = {
    isFocused: false
  }
  fontCanvasRef = React.createRef<HTMLCanvasElement>();
  ctx: CanvasRenderingContext2D | null | undefined = null;
  /////////////////////////////////////////////
  componentDidUpdate() {
    this.ctx = this.fontCanvasRef?.current?.getContext('2d');
    if (this.ctx) FontToolUtil.drawImageAndGetSVG(this.ctx, this.props.args['font_glyph_code']);
  }
  /////////////////////////////////////////////
  public render = (): ReactNode => {
    const { theme } = this.props
    const fontCanvasStyle: React.CSSProperties = {}
    fontCanvasStyle.backgroundImage = 'url(data:image/svg+xml;base64,' + btoa(FontToolUtil.constant.svgStrGrid) + ')';
    if (theme) {
      fontCanvasStyle.color = theme.textColor;
    }
    return (
      <div>
        <canvas id='font-canvas' width='500' height='500'
          onMouseEnter={this.onMouseEnter}
          onMouseLeave={this.onMouseLeave}
          onClick={this.onClick}
          style={fontCanvasStyle}
          ref={this.fontCanvasRef}/>
        <canvas id='scratch-canvas' width='500' height='500'/>
        <img id='scratch-img' alt='scratch'/>
      </div>
    )
  }
  private onClick = (): void => {
    Streamlit.setComponentValue(this.props.args['font_glyph_code'])
    this.forceUpdate();
  }
  private onMouseEnter = (): void => {
    this.setState({ isFocused: true })
  }
  private onMouseLeave = (): void => {
    this.setState({ isFocused: false })
  }
}
export default withStreamlitConnection(FontTool)
