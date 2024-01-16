import json
##########################################
# Static class ColibriTextReplacer
##########################################
class ColibriTextReplacer:
  @staticmethod
  def general_in_place_array_function(arr, func, only_leaf_index=-1):
    for i in range(len(arr)):
      if isinstance(arr[i], list):
        ColibriTextReplacer.general_in_place_array_function(arr[i], func, only_leaf_index)
      elif only_leaf_index < 0 or i == only_leaf_index:
        arr[i] = func(arr[i])
  @staticmethod
  def add_escaping(arr, only_leaf_index=-1):
    ColibriTextReplacer.general_in_place_array_function(arr, lambda s: ''.join(['\\' + c for c in s]), only_leaf_index)
  @staticmethod
  def remove_escaping(arr, only_leaf_index=-1):
    ColibriTextReplacer.general_in_place_array_function(arr, lambda s: s.replace('\\', ''), only_leaf_index)
  @staticmethod
  def symbolize_whitespace(arr, only_leaf_index=-1):
    return ColibriTextReplacer.general_in_place_array_function(arr, lambda s: '_🛑_' + s.replace('\n', '_⚠_').replace(' ', '_') + '_🛑_', only_leaf_index)
  @staticmethod
  def restore_whitespace(arr, only_leaf_index=-1):
    return ColibriTextReplacer.general_in_place_array_function(arr, lambda s: s.replace('_🛑_', '').replace('_🛑', '').replace('🛑_', '').replace('🛑', '').replace('_⚠_', '\n').replace('_⚠', '\n').replace('⚠_', '\n').replace('⚠', '\n').replace('_', ' '), only_leaf_index)
  @staticmethod
  def symbolize_special_characters(arr, only_leaf_index=-1):
    return ColibriTextReplacer.general_in_place_function(arr, lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), only_leaf_index)
  @staticmethod
  def restore_special_characters(arr, only_leaf_index=-1):
    return ColibriTextReplacer.general_in_place_function(arr, lambda s: s.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&'), only_leaf_index)
  @staticmethod
  def init(str_arr_replacement_map, section):
    r = [line.split() for line in str_arr_replacement_map.split('\n') if line.strip()]
    for j in range(len(r)):
      r[j] = [pair.split(',') for pair in r[j]]
    i_curr_section = -1
    for i_line in range(len(r)):
      if len(r[i_line]) == 1 and r[i_line][0][0] == '====SECTION':
        section[r[i_line][0][1]] = {'index': i_curr_section + 1, 'firstLine': i_line}
    if 'MAIN' not in section:
      section['MAIN'] = {'index': 0, 'firstLine': -1}
    ColibriTextReplacer.add_escaping(r, 0)
    return r
  @staticmethod
  def run(arr_page, i_page=0, arr_replace=None, section=None):
    ColibriTextReplacer.symbolize_whitespace(arr_page, i_page)
    ColibriTextReplacer.add_escaping(arr_page, i_page)
    if not section or 'MAIN' not in section:
      return
    for i_line_saved, i_line in enumerate(range(section['MAIN']['firstLine'] + 1, len(arr_replace))):
      if len(arr_replace[i_line]) == 1:
        hyphen_split = arr_replace[i_line][0][0].replace('\\', '').split('-')
        if hyphen_split[0] == '====RUN':
          num_repetitions = int(hyphen_split[1]) if len(hyphen_split) > 1 else 1
          section_title = arr_replace[i_line][0][1]
          i_line_saved = i_line
          for _ in range(num_repetitions):
            next_section_title = next(key for key, value in section.items() if value['index'] == section[section_title]['index'] + 1)
            for i_line in range(section[section_title]['firstLine'] + 1, section[next_section_title]['firstLine']):
              for pair_on_line in arr_replace[i_line]:
                arr_page[i_page] = arr_page[i_page].replace(pair_on_line[0], pair_on_line[1])
          i_line = i_line_saved + 1
      for pair_on_line in arr_replace[i_line]:
        arr_page[i_page] = arr_page[i_page].replace(pair_on_line[0], pair_on_line[1])
    ColibriTextReplacer.remove_escaping(arr_page, i_page)
    ColibriTextReplacer.restore_whitespace(arr_page, i_page)
##########################################
# Static class ColibriFileManager
##########################################
class ColibriFileManager:
  @staticmethod
  def new_project():
    return {
      'bookPageNumber': 0,
      'bookPages': [''],
      'graphReplace': '',
      'phoneReplace': '',
      'fontGlyphCode': '',
      'fontKerningCode': '',
      'fontOptions': {
        'pen': 'medium',
        'size': 'large',
        'space': '.5',
        'style': 'plain',
        'weight': 'bold',
        'direction': 'right-down',
      }
    }
  @staticmethod
  def load_url_file(url=None):
    ret = {}
    input_data = {}
    f = open(url, 'r')
    text = f.read()
    f.close()
    input_data = json.loads(text.split('<desc>')[1].split('</desc>')[0] if '<desc>' in text else '{}')
    if input_data.get('bookPages'):
      ret = input_data
    else:
      if text:
        ret = {
          'bookPageNumber': 0,
          'bookPages': input_data.get('user-text', '').split('{br}\n') or [input_data.get('user-text', '')],
          'graphReplace': input_data.get('grapheme-map', ''),
          'phoneReplace': input_data.get('phoneme-map', ''),
          'fontGlyphCode': input_data.get('font-code', ''),
          'fontKerningCode': input_data.get('kerning-map', ''),
          'fontOptions': {
            'pen': input_data.get('pen', 'medium'),
            'size': input_data.get('size', 'large'),
            'space': input_data.get('space', '.5'),
            'style': input_data.get('style', 'plain'),
            'weight': input_data.get('weight', 'bold'),
            'direction': input_data.get('direction', 'right-down'),
          }
        }
      else:
        raise ValueError('File at URL unreadable or does not exist')
    return ret
##########################################
# Static class ColibriBook
##########################################
class ColibriBook:
  def __init__(self):
    self.font = {'url': ''}
    self.graph = {'section': {}}
    self.phone = {'section': {}}
    self.source = {'fontOptions': {}}
    self.source.update(ColibriFileManager.new_project())
  ##########################################
  def init(self, library_url, book_title):
    self.title = book_title
    self.library_url = library_url
    url = library_url + book_title + '.svg'
    self.font['url'] = url
    self.graph['section'] = {}
    self.phone['section'] = {}
    self.source['fontOptions'] = {}
    self.source.update(ColibriFileManager.load_url_file(url))
    self.graph['arrReplace'] = ColibriTextReplacer.init(self.source['graphReplace'], self.graph['section'])
    self.phone['arrReplace'] = ColibriTextReplacer.init(self.source['phoneReplace'], self.phone['section'])
    self.font['arrGlyphCode'] = self.source['fontGlyphCode'].split('\n') if self.source['fontGlyphCode'] else []
    self.font['arrKerningCode'] = self.source['fontKerningCode'].split('\n') if self.source['fontKerningCode'] else []
  ##########################################
  def run(self):
    num_book_pages = len(self.source['bookPages']) if self.source['bookPages'] else 1
    if self.source['bookPageNumber'] >= num_book_pages:
      self.source['bookPageNumber'] = num_book_pages - 1
    self.graph['text'] = [self.source['bookPages'][self.source['bookPageNumber']]]
    self.phone['text'] = [self.source['bookPages'][self.source['bookPageNumber']]]
    ColibriTextReplacer.run(self.graph['text'], 0, self.graph['arrReplace'], self.graph['section'])
    ColibriTextReplacer.run(self.phone['text'], 0, self.phone['arrReplace'], self.phone['section'])
