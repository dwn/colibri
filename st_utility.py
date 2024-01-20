from streamlit import markdown
#Reads multiple files from an array of filenames
def read(file_paths):
  contents = []
  for file_path in file_paths:
    try:
      with open(file_path, 'r') as file:
        content = file.read()
        contents.append(content)
    except FileNotFoundError:
      contents.append(None)
  return contents
#Values referenced by spectrum()
num_spectrum_colors = 7
spectrum_code = [
    '610061', '640066', '67006a', '6a006f', '6d0073', '6f0077', '72007c', '740080', '760084', '780088', '79008d', '7b0091', '7c0095', '7e0099', '7f009d', '8000a1', '8100a5', '8100a9', '8200ad', '8200b1', '8300b5', '8300b9', '8300bc', '8300c0', '8200c4', '8200c8', '8100cc', '8100cf', '8000d3', '7f00d7', '7e00db', '7c00de', '7b00e2', '7900e6', '7800e9', '7600ed', '7400f1', '7100f4', '6f00f8', '6d00fb',
    '6a00ff', '6600ff', '6100ff', '5d00ff', '5900ff', '5400ff', '5000ff', '4b00ff', '4600ff', '4200ff', '3d00ff', '3800ff', '3300ff', '2e00ff', '2800ff', '2300ff', '1d00ff', '1700ff', '1100ff', '0a00ff', '0000ff', '000bff', '0013ff', '001bff', '0022ff', '0028ff', '002fff', '0035ff', '003bff', '0041ff', '0046ff', '004cff', '0051ff', '0057ff', '005cff', '0061ff', '0066ff', '006cff', '0071ff', '0076ff',
    '007bff', '007fff', '0084ff', '0089ff', '008eff', '0092ff', '0097ff', '009cff', '00a0ff', '00a5ff', '00a9ff', '00aeff', '00b2ff', '00b7ff', '00bbff', '00c0ff', '00c4ff', '00c8ff', '00cdff', '00d1ff', '00d5ff', '00daff', '00deff', '00e2ff', '00e6ff', '00eaff', '00efff', '00f3ff', '00f7ff', '00fbff', '00ffff', '00fff5', '00ffea', '00ffe0', '00ffd5', '00ffcb', '00ffc0', '00ffb5', '00ffa9', '00ffa4',
    '00ffa0', '00ff87', '00ff7b', '00ff6e', '00ff61', '00ff54', '00ff46', '00ff38', '00ff28', '00ff17', '00ff00', '09ff00', '0fff00', '15ff00', '1aff00', '1fff00', '24ff00', '28ff00', '2dff00', '31ff00', '36ff00', '3aff00', '3eff00', '42ff00', '46ff00', '4aff00', '4eff00', '52ff00', '56ff00', '5aff00', '5eff00', '61ff00', '65ff00', '69ff00', '6cff00', '70ff00', '73ff00', '77ff00', '7bff00', '7eff00',
    '81ff00', '85ff00', '88ff00', '8cff00', '8fff00', '92ff00', '96ff00', '99ff00', '9cff00', 'a0ff00', 'a3ff00', 'a6ff00', 'a9ff00', 'adff00', 'b0ff00', 'b3ff00', 'b6ff00', 'b9ff00', 'bdff00', 'c0ff00', 'c3ff00', 'c6ff00', 'c9ff00', 'ccff00', 'cfff00', 'd2ff00', 'd5ff00', 'd8ff00', 'dbff00', 'deff00', 'e1ff00', 'e4ff00', 'e7ff00', 'eaff00', 'edff00', 'f0ff00', 'f3ff00', 'f6ff00', 'f9ff00', 'fcff00',
    'ffff00', 'fffc00', 'fff900', 'fff600', 'fff200', 'ffef00', 'ffec00', 'ffe900', 'ffe600', 'ffe200', 'ffdf00', 'ffdc00', 'ffd900', 'ffd500', 'ffd200', 'ffcf00', 'ffcb00', 'ffc800', 'ffc500', 'ffc100', 'ffbe00', 'ffbb00', 'ffb700', 'ffb400', 'ffb000', 'ffad00', 'ffa900', 'ffa600', 'ffa200', 'ff9f00', 'ff9b00', 'ff9800', 'ff9400', 'ff9100', 'ff8d00', 'ff8900', 'ff8600', 'ff8200', 'ff7e00', 'ff7b00',
    'ff7700', 'ff7300', 'ff6f00', 'ff6b00', 'ff6700', 'ff6300', 'ff5f00', 'ff5b00', 'ff5700', 'ff5300', 'ff4f00', 'ff4b00', 'ff4600', 'ff4200', 'ff3e00', 'ff3900', 'ff3400', 'ff3000', 'ff2b00', 'ff2600', 'ff2100', 'ff1b00', 'ff1600', 'ff1000', 'ff0900', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000',
    'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'ff0000', 'fb0000', 'fa0000', 'f60000',
    'f20000', 'f10000', 'ed0000', 'e90000', 'e80000', 'e40000', 'e00000', 'de0000', 'db0000', 'd70000', 'd30000', 'd10000', 'ce0000', 'ca0000', 'c80000', 'c40000', 'c00000', 'be0000', 'ba0000', 'b70000', 'b50000', 'b10000', 'ad0000', 'ab0000', 'a70000', 'a30000', '9f0000', '9d0000', '990000', '950000', '930000', '8f0000', '8a0000', '880000', '840000', '800000', '7e0000', '7a0000', '750000',
    '730000', '6f0000', '6a0000', '660000', '640000', '580000', '420000', '160000'
]
#Defines a color octave with numColors divisions, starting with baseColor_THz
#Optional return type: 'hex' (default), 'THz' (frequency), 'nm' (wavelength)
#(Some wavelengths to target ±20 nm: green 525, cyan 500, yellow 580, orange 610)
#static color(colorIndex, returnType = 'hex', numColors = 7, baseColor_THz = 415, indexOffset = 0) { //GOOD! [gray-crimson]
#static color(colorIndex, returnType = 'hex', numColors = 8, baseColor_THz = 420, indexOffset = 0) { //GOOD! [gray-crimson]
#static color(colorIndex, returnType = 'hex', numColors = 12, baseColor_THz = 420, indexOffset = 0) { //GOOD! [gray-crimson]
#static color(colorIndex, returnType = 'hex', numColors = 7, baseColor_THz = 440, indexOffset = -1) { //PRETTY GOOD! [gray-red]
#static color(colorIndex, returnType = 'hex', numColors = 8, baseColor_THz = 455, indexOffset = -1) { //GOOD! [white-red]
#static color(colorIndex, returnType = 'hex', numColors = 7, baseColor_THz = 482, indexOffset = -2) { //NO: OCTAVE STARTS WITH ORANGE [white-orange]
#static color(colorIndex, returnType = 'hex', numColors = 8, baseColor_THz = 482, indexOffset = -2) { //NO: TWO GREENS [gray-crimson]
def spectrum(color_index, return_type='hex', base_color_thz=420, index_offset=0):
    color_index += index_offset
    c_over_1000 = 299792.458
    base_color_nm = c_over_1000 / base_color_thz  # nm = 1000 * c / THz
    diff_per_index_nm = base_color_nm / (2 * num_spectrum_colors)
    nm = round(base_color_nm - color_index * diff_per_index_nm)
    if return_type == 'nm':
        return round(nm)
    if return_type == 'THz':
        return round(c_over_1000 / nm)
    if nm >= 740:
        return '#000000'
    if nm <= 380 - 2 * diff_per_index_nm:
        return '#ffffff'
    if nm < 380:
        param = (1 / 3) * (color_index - (num_spectrum_colors - 2))
        hex_val = hex(int(255 * param))[2:]
        hex_val = '#' + hex_val + hex_val + hex_val
        return hex_val
    if nm < 380 + diff_per_index_nm:
        code = spectrum_code[nm - 380]
        ro = int(code[0:2], 16)
        go = int(code[2:4], 16)
        bo = int(code[4:6], 16)
        param = (1 / 3) * (color_index - (num_spectrum_colors - 2))
        r_hex = hex(int(ro * (1 - param) + 255 * param))[2:]
        g_hex = hex(int(go * (1 - param) + 255 * param))[2:]
        b_hex = hex(int(bo * (1 - param) + 255 * param))[2:]
        if len(r_hex) < 2:
            r_hex = '0' + r_hex
        if len(g_hex) < 2:
            g_hex = '0' + g_hex
        if len(b_hex) < 2:
            b_hex = '0' + b_hex
        return '#' + r_hex + g_hex + b_hex
    return '#' + spectrum_code[nm - 380]
#Set hex colors from palette
def set_colors(palette):
  global color
  color = {}
  for key, val in palette.items():
    if isinstance(val, int):
      # Single index, add the hex color directly
      color[key] = spectrum(val)
    elif isinstance(val, list):
      # Blending, calculate the average hex color
      num_colors = len(val)
      blended_color = '#'
      r_total, g_total, b_total = 0, 0, 0
      for i in val:
        hex_color = spectrum(i)
        r_total += int(hex_color[1:3], 16)
        g_total += int(hex_color[3:5], 16)
        b_total += int(hex_color[5:7], 16)
      blended_color += format(r_total // num_colors, '02x')
      blended_color += format(g_total // num_colors, '02x')
      blended_color += format(b_total // num_colors, '02x')
      color[key] = blended_color
#Display spectrum
def show_spectrum():
  markdown('###### spectrum')
  for i in range(-1, num_spectrum_colors + 2):
    markdown('<div class="color" style="background-color:{hex}; text-shadow:0 0 9px black">{index} | {hex} | {nm} nm | {THz} THz</div>'.format(index=i, hex=spectrum(i), nm=spectrum(i, 'nm'), THz=spectrum(i, 'THz')), unsafe_allow_html=True)
#Display hex colors from palette
def show_colors():
  markdown('###### color')
  i = 0
  for key, val in color.items():
    markdown('<div class="color" style="background-color:{hex}; text-shadow:0 0 9px black">{name} | {index} | {hex}</div>'.format(name=key, index=i, hex=val), unsafe_allow_html=True)
    i += 1
