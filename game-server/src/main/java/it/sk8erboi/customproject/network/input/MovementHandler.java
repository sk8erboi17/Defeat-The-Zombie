package it.sk8erboi.customproject.network.input;

import it.sk8erboi.customproject.api.network.pipeline.out.PipelineOut;
import it.sk8erboi.customproject.api.network.pipeline.out.PipelineOutBuilder;
import it.sk8erboi.customproject.network.output.StringServerOut;
import it.sk8erboi.customproject.world.User;
import it.sk8erboi.customproject.services.NetworkService;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;

@RequiredArgsConstructor
public class MovementHandler implements Handler {

    private final NetworkService networkService;

    @Override
    @SneakyThrows

    public void handle(Object request) {

        if (request instanceof String) {
            String string = request.toString();
            if (string.startsWith("movement:")) {
                string = string.substring("movement:".length());

                String name = string.split(":")[0];

                double x_coordinate;
                double y_coordinate;
                try {
                     x_coordinate = Double.parseDouble(string.split(":")[1]);
                     y_coordinate = Double.parseDouble(string.split(":")[2]);
                }catch (NumberFormatException e) {
                    return;
                }

                //TODO CHECK NULL
                User targetUser = networkService.getUserByName(name);
                targetUser.setX_coordinate(x_coordinate);
                targetUser.setY_coordinate(y_coordinate);

                for (User user : networkService.getUserList()) {
                    if(user.equals(targetUser)) continue;

                    PipelineOut pipelineOut = new PipelineOutBuilder(user.getAsynchronousSocketChannel()).allocateDirect(true).setBufferSize(4096).buildSocket();
                    pipelineOut.handleRequest(new StringServerOut("movement:" + name +":" + targetUser.getX_coordinate() + ":" + targetUser.getY_coordinate()));

                }


            }


        }
    }
}
