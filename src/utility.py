import re
import glob
import os
import io

import pdfminer.converter
import pdfminer.layout
import pdfminer.pdfinterp
import pdfminer.pdfpage
import pdfminer.pdfparser

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


    @classmethod
    def is_invalid_text(cls, text, ch_lowerlimit=5, word_lowerlimit=3, word_upperlimit=20):
        """
        textを構成する単語の最大文字列がch_lowerlimit未満であるか、
        もしくは、textを構成する単語数がword_lowerlimit未満の場合Trueを返します。
        また、word_upperlimit以上の文字数の単語が含まれる場合もTrueを返します。
        * グラフ中の文字列は全て結合した状態で表示されることもあるため、極端に長い単語を含む場合は無効な文章とする。

        文章として意味のなさそうなものを削除する場合などに使用します。

        >>> Utility.is_invalid_text("aaa bbbbb cc")
        False
        >>> Utility.is_invalid_text("aaa bbbbb cc", ch_lowerlimit=6)
        True
        >>> Utility.is_invalid_text("aaa bbbbb cc", word_lowerlimit=4)
        True
        >>> Utility.is_invalid_text(" a b c d e f g h ", word_lowerlimit=4)
        True
        >>> Utility.is_invalid_text("aaa bbbbbbbbbbbbbbbbbbbb cc")
        True
        """
        words = text.split()
        max_word_length = max([len(word) for word in words]) 
        if (len(words) < word_lowerlimit) or (max_word_length < ch_lowerlimit) or (max_word_length >= word_upperlimit):
            return True
        else:
            return False

    #TODO: テスト方法に迷ったので、いったんテストはペンディング。後でテスト方法を検討する。
    @classmethod
    def load_pdf_texts(cls, filepath, newline='\n'):
        """
        PDFからテキストデータを読み込み、改行コードで区切ったテキストのリストを返します。
        改行コードはnewlineで指定できます。
        """
        output = io.StringIO()
        with open(filepath, 'rb') as fin:
            parser = pdfminer.pdfparser.PDFParser(fin)
            doc = pdfminer.pdfdocument.PDFDocument(parser)
            rsrcmgr = pdfminer.pdfinterp.PDFResourceManager()
            device = pdfminer.converter.TextConverter(rsrcmgr, output,laparams=pdfminer.layout.LAParams())
            interpreter = pdfminer.pdfinterp.PDFPageInterpreter(rsrcmgr, device)
            for page in pdfminer.pdfpage.PDFPage.create_pages(doc):
                interpreter.process_page(page)
        return output.getvalue().split(newline)



if __name__ == '__main__':
    import doctest
    doctest.testmod()