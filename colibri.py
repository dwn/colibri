import json
##########################################
# Static class Text_Replacer
##########################################
class Text_Replacer:
  @staticmethod
  def general_in_place_array_function(arr, func, only_leaf_index=-1):
    for i in range(len(arr)):
      if isinstance(arr[i], list):
        Text_Replacer.general_in_place_array_function(arr[i], func, only_leaf_index)
      elif only_leaf_index < 0 or i == only_leaf_index:
        arr[i] = func(arr[i])
  @staticmethod
  def add_escaping(arr, only_leaf_index=-1):
    Text_Replacer.general_in_place_array_function(arr, lambda s: ''.join(['\\' + c for c in s]), only_leaf_index)
  @staticmethod
  def remove_escaping(arr, only_leaf_index=-1):
    Text_Replacer.general_in_place_array_function(arr, lambda s: s.replace('\\', ''), only_leaf_index)
  @staticmethod
  def symbolize_whitespace(arr, only_leaf_index=-1):
    return Text_Replacer.general_in_place_array_function(arr, lambda s: '_🛑_' + s.replace('\n', '_⚠_').replace(' ', '_') + '_🛑_', only_leaf_index)
  @staticmethod
  def restore_whitespace(arr, only_leaf_index=-1):
    return Text_Replacer.general_in_place_array_function(arr, lambda s: s.replace('_🛑_', '').replace('_🛑', '').replace('🛑_', '').replace('🛑', '').replace('_⚠_', '\n').replace('_⚠', '\n').replace('⚠_', '\n').replace('⚠', '\n').replace('_', ' '), only_leaf_index)
  @staticmethod
  def symbolize_special_characters(arr, only_leaf_index=-1):
    return Text_Replacer.general_in_place_function(arr, lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), only_leaf_index)
  @staticmethod
  def restore_special_characters(arr, only_leaf_index=-1):
    return Text_Replacer.general_in_place_function(arr, lambda s: s.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&'), only_leaf_index)
  @staticmethod
  def init(str_arr_replacement_map, section):
    r = [line.split() for line in str_arr_replacement_map.split('\n') if line.strip()]
    for j in range(len(r)):
      r[j] = [pair.split(',') for pair in r[j]]
    i_curr_section = -1
    for i_line in range(len(r)):
      if len(r[i_line]) == 1 and r[i_line][0][0] == '====SECTION':
        section[r[i_line][0][1]] = {'index': i_curr_section + 1, 'first_line': i_line}
    if 'MAIN' not in section:
      section['MAIN'] = {'index': 0, 'first_line': -1}
    Text_Replacer.add_escaping(r, 0)
    return r
  @staticmethod
  def run(arr_page, i_page=0, arr_replace=None, section=None):
    Text_Replacer.symbolize_whitespace(arr_page, i_page)
    Text_Replacer.add_escaping(arr_page, i_page)
    if not section or 'MAIN' not in section:
      return
    for i_line_saved, i_line in enumerate(range(section['MAIN']['first_line'] + 1, len(arr_replace))):
      if len(arr_replace[i_line]) == 1:
        hyphen_split = arr_replace[i_line][0][0].replace('\\', '').split('-')
        if hyphen_split[0] == '====RUN':
          num_repetitions = int(hyphen_split[1]) if len(hyphen_split) > 1 else 1
          section_title = arr_replace[i_line][0][1]
          i_line_saved = i_line
          for _ in range(num_repetitions):
            next_section_title = next(key for key, value in section.items() if value['index'] == section[section_title]['index'] + 1)
            for i_line in range(section[section_title]['first_line'] + 1, section[next_section_title]['first_line']):
              for pair_on_line in arr_replace[i_line]:
                arr_page[i_page] = arr_page[i_page].replace(pair_on_line[0], pair_on_line[1])
          i_line = i_line_saved + 1
      for pair_on_line in arr_replace[i_line]:
        arr_page[i_page] = arr_page[i_page].replace(pair_on_line[0], pair_on_line[1])
    Text_Replacer.remove_escaping(arr_page, i_page)
    Text_Replacer.restore_whitespace(arr_page, i_page)
##########################################
# Static class File_Manager
##########################################
class File_Manager:
  @staticmethod
  def new_project():
    return {
      'book_page_number': 0,
      'book_pages': [''],
      'graph_replace': '',
      'phone_replace': '',
      'font_glyph_code': '',
      'font_kerning_code': '',
      'font_options': {
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
    if input_data.get('book_pages'):
      ret = input_data
    else:
      if text:
        ret = {
          'book_page_number': 0,
          'book_pages': input_data.get('user-text', '').split('{br}\n') or [input_data.get('user-text', '')],
          'graph_replace': input_data.get('grapheme-map', ''),
          'phone_replace': input_data.get('phoneme-map', ''),
          'font_glyph_code': input_data.get('font-code', ''),
          'font_kerning_code': input_data.get('kerning-map', ''),
          'font_options': {
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
# Static class Book
##########################################
class Book:
  def __init__(self):
    self.font = {'url': ''}
    self.graph = {'section': {}}
    self.phone = {'section': {}}
    self.source = {'font_options': {}}
    self.source.update(File_Manager.new_project())
  ##########################################
  def init(self, library_url, book_title):
    self.title = book_title
    self.library_url = library_url
    url = library_url + book_title + '.svg'
    self.font['url'] = url
    self.graph['section'] = {}
    self.phone['section'] = {}
    self.source['font_options'] = {}
    self.source.update(File_Manager.load_url_file(url))
    self.graph['arr_replace'] = Text_Replacer.init(self.source['graph_replace'], self.graph['section'])
    self.phone['arr_replace'] = Text_Replacer.init(self.source['phone_replace'], self.phone['section'])
    self.font['arr_glyph_code'] = self.source['font_glyph_code'].split('\n') if self.source['font_glyph_code'] else []
    self.font['arr_kerning_code'] = self.source['font_kerning_code'].split('\n') if self.source['font_kerning_code'] else []
  ##########################################
  def run(self):
    num_book_pages = len(self.source['book_pages']) if self.source['book_pages'] else 1
    if self.source['book_page_number'] >= num_book_pages:
      self.source['book_page_number'] = num_book_pages - 1
    self.graph['text'] = [self.source['book_pages'][self.source['book_page_number']]]
    self.phone['text'] = [self.source['book_pages'][self.source['book_page_number']]]
    Text_Replacer.run(self.graph['text'], 0, self.graph['arr_replace'], self.graph['section'])
    Text_Replacer.run(self.phone['text'], 0, self.phone['arr_replace'], self.phone['section'])
  ##########################################
  def __getitem__(self, key):
    if key == 'graph':
      return self.graph
    elif key == 'phone':
      return self.phone
    elif key == 'font':
      return self.font
    elif key == 'source':
      return self.source
    # Add more cases as needed
    else:
      raise KeyError(f"Invalid key: {key}")
