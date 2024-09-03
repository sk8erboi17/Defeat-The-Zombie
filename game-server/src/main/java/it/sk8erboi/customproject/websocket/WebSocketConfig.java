package it.sk8erboi.customproject.websocket;

import it.sk8erboi.customproject.services.NetworkService;
import it.sk8erboi.customproject.services.LoggingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    @Autowired
    private LoggingService loggingService;

    @Autowired
    private NetworkService networkService;

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(new NotificationWebSocketHandler(loggingService,networkService), "/websocket").setAllowedOrigins("*");
    }

}