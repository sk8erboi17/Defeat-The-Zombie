package it.sk8erboi.customproject.network.input;

import it.sk8erboi.customproject.api.network.pipeline.out.PipelineOut;
import it.sk8erboi.customproject.api.network.pipeline.out.PipelineOutBuilder;
import it.sk8erboi.customproject.network.output.StringServerOut;
import it.sk8erboi.customproject.services.EnemyService;
import it.sk8erboi.customproject.services.NetworkService;
import it.sk8erboi.customproject.services.LoggingService;
import it.sk8erboi.customproject.world.User;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;

import java.util.UUID;

@RequiredArgsConstructor
public class KillHandler implements Handler{

    private final LoggingService loggingService;

    private final NetworkService networkService;

    private final EnemyService enemyService;

    @SneakyThrows
    @Override
    public void handle(Object request) {
        if(request instanceof String){
            String string = request.toString();
            if(string.startsWith("kill:")){
                string = string.substring("kill:".length());
                String namePlayer = string.split(":")[0];
                UUID uuidMob = UUID.fromString(string.split(":")[1]);
                enemyService.remove(enemyService.getEnemyByUuid(uuidMob));

                for (User user : networkService.getUserList()) {
                    if (user.getUsername().equalsIgnoreCase(namePlayer)) {
                        continue;
                    }

                    PipelineOut pipelineOut = new PipelineOutBuilder(user.getAsynchronousSocketChannel()).allocateDirect(true).setBufferSize(4096).buildSocket();
                    pipelineOut.handleRequest(new StringServerOut("remove_enemy:" + uuidMob));
                }

            }
        }
    }
}
