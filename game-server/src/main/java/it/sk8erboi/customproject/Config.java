package it.sk8erboi.customproject;

import it.sk8erboi.customproject.api.Listener;
import it.sk8erboi.customproject.api.listeners.input.AsyncInputSocket;
import it.sk8erboi.customproject.api.listeners.output.AsyncChannelSocket;
import lombok.SneakyThrows;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Scope;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.net.InetSocketAddress;
import java.nio.channels.AsynchronousServerSocketChannel;
import java.nio.channels.AsynchronousSocketChannel;

@Configuration
public class Config {

    @SneakyThrows
    @Bean
    @Scope("singleton")
    //get che input channel of the server
    public AsynchronousServerSocketChannel inputChannel(){
        return AsyncInputSocket.createInput(new InetSocketAddress(8082));
    }

    @Bean
    @Scope("singleton")
    //get the listener of events of the server, that listen from the clients
    public Listener listener(){
        return Listener.getInstance();
    }
}
