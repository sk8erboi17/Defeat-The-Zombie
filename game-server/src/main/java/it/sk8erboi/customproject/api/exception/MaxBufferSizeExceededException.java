package it.sk8erboi.customproject.api.exception;

public class MaxBufferSizeExceededException extends Exception {

    public MaxBufferSizeExceededException() {
        super("Packet rejected: buffer size exceeds maxBufferSize!");
    }
}
