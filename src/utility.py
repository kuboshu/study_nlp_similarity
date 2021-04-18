import re
import glob
import os

class UtilityError(Exception):
    pass

class Utility:

    @classmethod
    def get_pdflist(cls, dirpath, limit=0, recursive=False):
        """
        指定されたディレクトリパス以下にあるpdf(拡張子が.pdf)を検索し、ソート済みのパスリストを返します。
        取得する最大のパス数をlimitで指定できます。limitに0を指定するとリミット数を無効化します。
        """
        search_pattern = os.path.join(os.path.abspath(dirpath), '*.pdf')
        if recursive:
            search_pattern = os.path.join(os.path.abspath(dirpath), '**', '*.pdf')
        
        if limit == 0:
            return sorted(glob.glob(search_pattern, recursive=recursive))
        elif limit > 0:
            path_list = []
            for filepath in sorted(glob.iglob(search_pattern, recursive=recursive)):
                path_list.append(filepath)
                if len(path_list) == limit:
                    break
            return path_list
        else:
            raise UtilityError(f'limit({limit})が不正 : 0以上の整数値を入れてください。')

    @classmethod
    def combine_spaces(cls, sentence):
        """
        >>> Utility.combine_spaces('  hoge    foo bar  ')
        ' hoge foo bar '
        """
        return re.sub(r'\s+', r' ', sentence)

    @classmethod
    def connect_texts(cls, txt0, txt1):
        """
        2つのテキスト(txt0, txt1)を半角スペースで結合します。
        また、txt0の最後の文字が「-」で終わっている場合は、「-」を削除して連結させます。
        文中に存在する「-」はそのまま残ります。
        結合後のテキストの前後の半角スペースは削除されます。
        
        >>> Utility.connect_texts('  aaa', 'bbb ')
        'aaa bbb'
        >>> Utility.connect_texts('aaa-', 'bbb')
        'aaabbb'
        >>> Utility.connect_texts('aaa-', 'b-bb')
        'aaab-bb'
        >>> Utility.connect_texts('aaa-', 'bbb-')
        'aaabbb-'
        """
        if re.search(r'(?<=-)$', txt0):
            connected_text =  re.sub(r'-$', '', txt0) + txt1
        else:
            connected_text = txt0 + " " + txt1
        return re.sub(r'(?:^\s*)|(?:\s*$)', '', connected_text)
    
    @classmethod
    def convert_number_to_word(cls, text, word="NUMBER"):
        """
        text中の数値データをwordで置き換えます。
        半角スペースが無く「,」「.」で連続した数値は１つの数値とみなされます。

        >>> Utility.convert_number_to_word('0.01%')
        'NUMBER%'
        >>> Utility.convert_number_to_word('0.01, 0.02, 0.03')
        'NUMBER, NUMBER, NUMBER'
        >>> Utility.convert_number_to_word("23230,010,020.03")
        'NUMBER'
        >>> Utility.convert_number_to_word("23230,,010,020.03")
        'NUMBER,NUMBER'
        """
        extract_pattern = r'(?:\d((\,(?!\s+))|(\.(?!\s+)))?)+'
        return re.sub(extract_pattern, word, text)



if __name__ == '__main__':
    import doctest
    doctest.testmod()