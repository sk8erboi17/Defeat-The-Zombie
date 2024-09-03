package it.sk8erboi.customproject.network.input;

import it.sk8erboi.customproject.api.network.pipeline.out.PipelineOut;
import it.sk8erboi.customproject.api.network.pipeline.out.PipelineOutBuilder;
import it.sk8erboi.customproject.network.output.StringServerOut;
import it.sk8erboi.customproject.world.User;
import it.sk8erboi.customproject.services.NetworkService;
import it.sk8erboi.customproject.services.LoggingService;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;

import java.nio.channels.AsynchronousSocketChannel;
import java.util.ArrayList;

@RequiredArgsConstructor
public class JoinHandler implements Handler {

    private final AsynchronousSocketChannel asynchronousSocketChannel;

    private final NetworkService networkService;

    private final LoggingService loggingService;

    @Override
    @SneakyThrows
    public void handle(Object request) {

        if (request instanceof String) {
            String string = request.toString();

            if (string.startsWith("join:")) {
                string = string.substring("join:".length()).replace(" joined", "");
                String name = string.split(":")[0];
                double x_coordinate = Double.parseDouble(string.split(":")[1]);
                double y_coordinate = Double.parseDouble(string.split(":")[2]);

                loggingService.addUpdate("[INFO] " + name + " joined at x:" + x_coordinate +"y:" + y_coordinate, false);
                User newPlayer = new User(asynchronousSocketChannel, name,x_coordinate, y_coordinate, 0);
                networkService.addUser(newPlayer);


                for (User user : networkService.getUserList()) {
                    if (user.getUsername().equalsIgnoreCase(name)) {
                        ArrayList<User> copyNetwork = new ArrayList<>(networkService.getUserList());
                        copyNetwork.remove(user);
                        for (User otherUsers : copyNetwork) {
                            PipelineOut pipelineOut = new PipelineOutBuilder(user.getAsynchronousSocketChannel()).allocateDirect(true).setBufferSize(4096).buildSocket();
                            pipelineOut.handleRequest(new StringServerOut("player_joined:" + otherUsers.getUsername() + ":" + otherUsers.getX_coordinate() + ":" + otherUsers.getY_coordinate()));
                        }
                        continue;
                    }

                    PipelineOut pipelineOut = new PipelineOutBuilder(user.getAsynchronousSocketChannel()).allocateDirect(true).setBufferSize(4096).buildSocket();
                    pipelineOut.handleRequest(new StringServerOut("player_joined:" + name +":" + user.getX_coordinate() + ":" + user.getY_coordinate()));
                }


            }


        }
    }
}
