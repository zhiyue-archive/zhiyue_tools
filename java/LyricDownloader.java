package com.kugou.BaseTemplateOCR.train;

import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.zip.Inflater;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.apache.commons.codec.binary.Base64;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

import com.kugou.BaseTemplateOCR.Utils.Files;


public class LyricDownloader {
	public static String URL_STRING = "http://3g.music.qq.com/fcgi-bin/3g_lyric";
	public static String POST_FORMAT = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><root><uid>%s</uid><sid>%s</sid><v>%s</v><cv>%s</cv><ct>%s</ct><udid>%s</udid><OpenUDID>%s</OpenUDID><cid>111</cid><music>%s</music><singer>%s</singer><album>%s</album></root>";
	public static String ENCODING = "UTF-8";
	
	public static void downLoad(String title,String singer,String rootPath) throws IOException, ParserConfigurationException, SAXException{

		String uid = "";
		String sid = "";
		String devid = "112cdsdfsd";
		title = new String(Base64.encodeBase64(title.getBytes()));
		singer = new String(Base64.encodeBase64(singer.getBytes()));
		String album = null;
		String postXml = String.format(POST_FORMAT, uid,sid,3,2001,1,devid,devid,title,singer,album);
		URL connectURL = new URL(URL_STRING);
		HttpURLConnection connection = (HttpURLConnection) connectURL.openConnection();
		connection.setDoInput(true);
		connection.setDoOutput(true);
		connection.setUseCaches(false);
		connection.setRequestMethod("POST");
		connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
		DataOutputStream dos = new DataOutputStream(connection.getOutputStream());	
		byte[] dataBuf = postXml.getBytes(ENCODING);
		dos.write(dataBuf, 0, dataBuf.length);
		dos.flush();
		dos.close();
		if (connection.getResponseCode() == 200) {
			InputStream is = connection.getInputStream();
			byte[] array = toByteArray(is);
			String[] lines = spliteLines(receiveData(true, array));		
			writeTofiles(rootPath, lines);
			
		}
	}
	
	//从InputStream 转换为byte数组
	public static byte[] toByteArray(InputStream is) throws IOException{
		ByteArrayOutputStream buffer = new ByteArrayOutputStream();
		int nRead;
		byte[] data = new byte[16384];
		while ((nRead = is.read(data, 0, data.length)) != -1) {
		  buffer.write(data, 0, nRead);
		}
		buffer.flush();
		return buffer.toByteArray();
	}
	
	public static String receiveData(Boolean succ,byte[] result) throws ParserConfigurationException, SAXException, IOException{
		//默认偏移量是5
		int offset = 5;
		int len = result.length - offset;
		byte[] tmpArray = new byte[len];
		System.arraycopy(result, offset, tmpArray, 0, len);	
		//解压压缩内容
		byte[] array = decompressByteArray(tmpArray);
		//再使用UTF8编码转换为文本
		String data = new String(array,ENCODING);
		
		String content = GetLyric(data);
		
		return content;
		
	}
	
	
	//解压压缩内容
	public static byte[] decompressByteArray(byte[] bytes){
		ByteArrayOutputStream baos = null;
		Inflater iflr = new Inflater();
		iflr.setInput(bytes);
		baos = new ByteArrayOutputStream();
		byte[] tmp = new byte[4 * 1024];
		try {
			while (!iflr.finished()) {
				int size = iflr.inflate(tmp);
				baos.write(tmp,0,size);
			}
		} catch (Exception e) {

		} finally{
			try {
				if (baos != null) {
					baos.close();
				}
			} catch (Exception e2) {

			}
		}
		return baos.toByteArray();
	}
	
	//传入base64加密的xml字符串，返回歌词字符串
	private static String GetLyric(String strContent) throws ParserConfigurationException, SAXException, IOException{
		//读取歌词内容XML文件
		DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
		DocumentBuilder db = dbf.newDocumentBuilder();
		Document document = db.parse(new InputSource(new StringReader(strContent)));//new StringBufferInputStream(strContent));
		Element bodyElement = (Element)document.getElementsByTagName("body").item(0);
		Element itemElement = (Element)bodyElement.getElementsByTagName("item").item(0);
		Element txtElement = (Element)itemElement.getElementsByTagName("txt").item(0);
		String strBase64Text = txtElement.getTextContent();
		//Base64解码内容
		byte[] array = Base64.decodeBase64(strBase64Text);	
		//通过UTF8编码转换成歌词内容
		strBase64Text = new String(array,ENCODING);
		//System.out.print(strBase64Text);
		return strBase64Text;
	}
	
	private static String[] spliteLines(String content){
		String[] lines = content.split("\n");
		ArrayList<String> sublines = new ArrayList<String>();
		
		for (int i = 0; i < lines.length; i++) {
			int beginIndex = lines[i].lastIndexOf(']') + 1;
			int lastIndex = lines[i].length()  > beginIndex ? lines[i].length() : beginIndex ; 
			
			String subLine = lines[i].substring(beginIndex, lastIndex );	
			if (!subLine.equals("")) {
				System.out.println(subLine);
				sublines.add(subLine);
			}		
		}
		return (String[]) sublines.toArray(new String[sublines.size()]);
	}
	
	private static void writeTofiles(String rootPath,String[] lines) throws IOException{
		String pathFormat = "%s/%s.txt";
		for (int i = 0; i < lines.length; i++) {	
			String fileString = String.format(pathFormat, rootPath,String.valueOf(i));
			File writeName = new File(fileString);
			writeName.createNewFile(); // 创建新文件 
			BufferedWriter out = new BufferedWriter(new FileWriter(writeName));  
			out.write(lines[i]);
			out.flush();
			out.close();
		}
	}
	
	public static void main(String[] args) throws IOException, ParserConfigurationException, SAXException{
		String title = "冰雨";
		String singer = "刘德华";
		String path = String.format("%s/%s-%s", "data/2015/template",title,singer);
		Files.mkdir(path);
		downLoad(title, singer,path);
	
	}
	
	
}
