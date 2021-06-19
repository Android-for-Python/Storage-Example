package org.kivy.storage;

import java.io.*;

public class StreamCopy {
    public StreamCopy(InputStream inputStream, String fileName)
	throws IOException, FileNotFoundException {
	int DEFAULT_BUFFER_SIZE = 8192;
	File file = new File(fileName);
	FileOutputStream outputStream = new FileOutputStream(file, false);
	int read;
	byte[] bytes = new byte[DEFAULT_BUFFER_SIZE];
	while ((read = inputStream.read(bytes)) != -1) {
	    outputStream.write(bytes, 0, read);
	}
	outputStream.flush();
	outputStream.close();
    }
}



