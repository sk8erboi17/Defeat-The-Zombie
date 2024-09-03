package it.sk8erboi.customproject.websocket;

import it.sk8erboi.customproject.api.network.pipeline.out.PipelineOut;
import it.sk8erboi.customproject.api.network.pipeline.out.PipelineOutBuilder;
import it.sk8erboi.customproject.network.output.StringServerOut;
import it.sk8erboi.customproject.world.User;
import it.sk8erboi.customproject.services.NetworkService;
import it.sk8erboi.customproject.services.LoggingService;
import lombok.AllArgsConstructor;
import lombok.SneakyThrows;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.handler.TextWebSocketHandler;

@AllArgsConstructor
public class NotificationWebSocketHandler extends TextWebSocketHandler {

    private LoggingService loggingService;

    private NetworkService networkService;

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) {
        System.out.println(message.getPayload());
        for (User user : networkService.getUserList()) {
            PipelineOut pipelineOut = new PipelineOutBuilder(user.getAsynchronousSocketChannel())
                    .allocateDirect(true).setBufferSize(4096).buildSocket();
            pipelineOut.handleRequest(new StringServerOut(message.getPayload()));
        }

    }

    @SneakyThrows
    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        for (Object notification : loggingService.getAllUpdates().keySet()) {
            session.sendMessage(new TextMessage(notification.toString()));
            loggingService.getAllUpdates().put(notification, true);
        }

        new Thread(() -> {
            try {
                while (true) {
                    if(!session.isOpen()) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                    for (Object notification : loggingService.getAllUpdates().keySet()) {
                        if(!loggingService.getAllUpdates().get(notification)){
                            session.sendMessage(new TextMessage(notification.toString()));
                            loggingService.getAllUpdates().put(notification, true);
                        }
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }).start();
    }
}
