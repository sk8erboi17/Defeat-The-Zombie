package it.sk8erboi.customproject.api;

import java.nio.channels.AsynchronousSocketChannel;


public interface ConnectionRequest {
    // Interface method to handle accepted connections
    void acceptConnection(AsynchronousSocketChannel socketChannel);
}
