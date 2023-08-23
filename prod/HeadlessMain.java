import java.io.File;

import heronarts.lx.LX;
import heronarts.lx.scheduler.LXScheduler;
import heronarts.lx.scheduler.LXScheduledProject;

public class HeadlessMain {
    static void comfortZone(LX lx) {
        LX.log("Hello from comfort zone");

        String home = System.getenv("PWD");
        File projectFile = new File(home, "pleasure_comfort_dancy_river.lxp");
        File projectFile2 = new File(home, "pleasure_comfort_birds.lxp");
    
        LX.log("Opening initial project file: " + projectFile);
        lx.openProject(projectFile);
        lx.openProject(projectFile2);
        lx.engine.start();
    
        // Control loop
        while(true) {
            try {
                Thread.sleep(5000);
                lx.setProject(projectFile, LX.ProjectListener.Change.TRY);
                LX.log("test project 1");
            
                Thread.sleep(5000);
                LX.log("test project 2");
                lx.setProject(projectFile, LX.ProjectListener.Change.TRY);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String args[]) {
        LX lx = new LX();

        if (args.length != 0) {     
            try {
                lx.openProject(new File(args[0]));
                lx.engine.start();
            } catch (Exception x) {
                LX.error(x);
            }
        } else {
            comfortZone(lx);
        }
    }
}