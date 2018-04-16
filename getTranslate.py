# 这是调用 谷歌翻译 接口，实现将英文pdf翻译成 中英双语

#coding=utf-8
import requests    
import execjs  
import sys
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

class PDF(): 

    def readPdf(self, pdfPath):
        fp = open(pdfPath, "rb")
        parser=PDFParser(fp)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize("")
        resource = PDFResourceManager()
        laparam = LAParams()
        device = PDFPageAggregator(resource,laparams=laparam)
        interpreter=PDFPageInterpreter(resource,device)
        result = ""
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout=  device.get_result()           
            for out in layout:
                if hasattr(out,"get_text"):
                    a = out.get_text().split("\n")
                    r = ""
                    for aa in a:
                        if len(aa)>1:
                            if (aa[0]>='A' and aa[0]<='Z') or (aa[0]>='a' and aa[0]<='z'):
                                r += ' '
                                r += aa
                        else:
                            r += '\n'
                    if r!='\t' and len(r.strip())>0:
                        result += r

        return result

    def PDF(self):  
        return "PDF" 

class Py4Js():  
      
    def __init__(self):  
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 
         
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 
     
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
        }; 
     
        function RL(a, b) { 
            var t = "a"; 
            var Yb = "+"; 
            for (var c = 0; c < b.length - 2; c += 3) { 
                var d = b.charAt(c + 2), 
                d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
                d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
                a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
            } 
            return a 
        } 
        """)  
          
    def getTk(self,text):  
        return self.ctx.call("TL",text)  

    def En2ChiJs(self):  
        return "En2ChiJs" 



class En2Chi:

    
    def translate(self,tk,content):     
  
        resChi = ''
        resEn = ''    
        param = {'tk': tk, 'q': content}  
      
        result = requests.get("""http://translate.google.cn/translate_a/single?client=t&sl=en 
            &tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss 
            &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)  
      
        for text in result.json():  
            if type(text) == list:               
                if text[0][0] != 'en':
                    for i in text:
                        a = 2
                        if(i[0] != None):
                            resChi += i[0]
                            resEn += i[1]
        print(resEn)
        print(resChi)
        return    

if __name__ == "__main__":      

    aPDFFile = PDF()
    content = aPDFFile.readPdf("1.pdf")

    js = Py4Js()
    ta = En2Chi()
    tk = js.En2ChiJs()  

    contents = content.split('\n')
    contentPart = ''
    for aContent in contents:
        contentPart = contentPart+(aContent+'\n')
        if len(contentPart) > 1800:        
            tk = js.getTk(contentPart)
            ta.translate(tk,contentPart) 
            contentPart = ''

    print("翻译结束")
