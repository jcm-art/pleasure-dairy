/**
 * Copyright 2020- Mark C. Slee, Heron Arts LLC
 *
 * This file is part of the LX Studio software library. By using
 * LX, you agree to the terms of the LX Studio Software License
 * and Distribution Agreement, available at: http://lx.studio/license
 *
 * Please note that the LX license is not open-source. The license
 * allows for free, non-commercial use.
 *
 * HERON ARTS MAKES NO WARRANTY, EXPRESS, IMPLIED, STATUTORY, OR
 * OTHERWISE, AND SPECIFICALLY DISCLAIMS ANY WARRANTY OF
 * MERCHANTABILITY, NON-INFRINGEMENT, OR FITNESS FOR A PARTICULAR
 * PURPOSE, WITH RESPECT TO THE SOFTWARE.
 *
 * @author Mark C. Slee <mark@heronarts.com>
 */

package heronarts.lx.app;

import java.io.File;
import heronarts.lx.LX;
import heronarts.lx.LXComponent;
import heronarts.lx.LXPlugin;
import heronarts.lx.LX.Flags;
import heronarts.lx.osc.LXOscComponent;
import heronarts.lx.parameter.BoundedParameter;
import heronarts.lx.studio.LXStudio;
import heronarts.p4lx.ui.component.UICollapsibleSection;
import heronarts.p4lx.ui.component.UIKnob;
import processing.core.PApplet;

/**
 * This is an example top-level class to build and run an LX Studio
 * application via an IDE. The main() method of this class can be
 * invoked with arguments to either run with a full Processing 4 UI
 * or as a headless command-line only engine.
 */
public class LXStudioApp extends PApplet implements LXPlugin {

  private static final String WINDOW_TITLE = "LX Studio";

  private static int WIDTH = 1280;
  private static int HEIGHT = 800;
  private static boolean FULLSCREEN = false;

  private static int WINDOW_X = 0;
  private static int WINDOW_Y = 0;

  private static boolean HAS_WINDOW_POSITION = false;

  @Override
  public void settings() {
    if (FULLSCREEN) {
      fullScreen(PApplet.P3D);
    } else {
      size(WIDTH, HEIGHT, PApplet.P3D);
    }
    pixelDensity(displayDensity());
  }

  @Override
  public void setup() {
    LXStudio.Flags flags = new LXStudio.Flags(this);
    flags.resizable = true;
    flags.useGLPointCloud = false;
    flags.startMultiThreaded = true;

    // NOTE: it seems like on Windows systems P4LX can end
    // up setting this to the "lib" folder depending on how
    // dependency JARs were loaded. Explicitly set it to "."
    // here and be sure to run explicitly from root folder
    flags.mediaPath = ".";

    new LXStudio(this, flags);
    this.surface.setTitle(WINDOW_TITLE);
    if (!FULLSCREEN && HAS_WINDOW_POSITION) {
      this.surface.setLocation(WINDOW_X, WINDOW_Y);
    }

  }

  public static class MyComponent extends LXComponent implements LXOscComponent {

    public final BoundedParameter param1 =
      new BoundedParameter("p1", 0)
      .setDescription("A global parameter that does something");

    public final BoundedParameter param2 =
      new BoundedParameter("p2", 0)
      .setDescription("A global parameter that does something else");

    public MyComponent(LX lx) {
      super(lx);
      addParameter("param1", this.param1);
      addParameter("param2", this.param2);
    }
  }

  // A global component for additional project-specific parameters, if desired
  public MyComponent myComponent;

  @Override
  public void initialize(LX lx) {
    // Here is where you should register any custom components or make modifications
    // to the LX engine or hierarchy. This is also used in headless mode, so note that
    // you cannot assume you are working with an LXStudio class or that any UI will be
    // available.

    // Register custom pattern and effect types
    lx.registry.addPattern(heronarts.lx.app.pattern.AppPattern.class);
    lx.registry.addPattern(heronarts.lx.app.pattern.AppPatternWithUI.class);
    lx.registry.addEffect(heronarts.lx.app.effect.AppEffect.class);

    // Create an instance of your global component and register it with the LX engine
    // so that it can be saved and loaded in project files
    this.myComponent = new MyComponent(lx);
    lx.engine.registerComponent("myComponent", this.myComponent);

  }

  public void initializeUI(LXStudio lx, LXStudio.UI ui) {
    // Here is where you may modify the initial settings of the UI before it is fully
    // built. Note that this will not be called in headless mode. Anything required
    // for headless mode should go in the raw initialize method above.
  }

  public static class UIMyComponent extends UICollapsibleSection {
    public UIMyComponent(LXStudio.UI ui, MyComponent myComponent) {
      super(ui, 0, 0, ui.leftPane.global.getContentWidth(), 80);
      setTitle("MY COMPONENT");

      new UIKnob(0, 0, myComponent.param1).addToContainer(this);
      new UIKnob(40, 0, myComponent.param2).addToContainer(this);
    }
  }

  public void onUIReady(LXStudio lx, LXStudio.UI ui) {
    // At this point, the LX Studio application UI has been built. You may now add
    // additional views and components to the UI hierarchy.
    new UIMyComponent(ui, this.myComponent)
    .addToContainer(ui.leftPane.global);
  }

  @Override
  public void draw() {
    // All handled by core LX engine, do not modify, method exists only so that Processing
    // will run a draw-loop.
  }

  /* PD headless code
   Modified from `public static void headless(Flags flags, File projectFile)` in LX.class
   Outline
   0. Precompile this App into JAR, call App from pdHost.service on Pi startup
   1. Load map of LX files -> matching sound files and timeout (different or same for each file)
      a. Can be different files based on Pi hostname so the different installations run smoothly
   2. Load lights + files
      a. Start headless LX engine with first .LXP file
      b. Start playing music
   3. Start timer
   4. Start GPIO loop that listens for button presses
   5. After button press or new timer, switch to a new project and play new sound
      a. Can be done with lx.openProject(newProjectFile);
      b. Causes a red flash on my test setup each time a new project is loaded. Trying to debug this.
         Caused in LXEngine.class line 1037 `this.mixer.loop(buffer.render, deltaMs);`

   TODO:
   1. How to load separate list of patterns, sounds, timeouts for different installations JSON input? (TBD)
   2. How to play 2x sound outputs using USB DAC and Pi and interface with Java (Rob)
   3. General GPIO in Java for button press (Zack)
   4. Can we easily load up 2x instances of LXStudio? (Zack)
      We should be able to create a simple LXStudio project for just RGB lighting the mural and run it in the main bash script that starts everything at the same time as the
   5. General .lxp scene design (Justion + All)
*/

  public static void pdHeadless(Flags flags, File projectFile) {
    LX.log("Starting LX headless engine " + LX.VERSION + "...");
    LX lx = new LX(flags);
    if (projectFile != null) {
      boolean isSchedule = projectFile.getName().endsWith(".lxs");
      if (!projectFile.exists()) {
        LX.error((isSchedule ? "Schedule" : "Project") + " file does not exist: " + projectFile);
      } else {
        if (isSchedule) {
          lx.preferences.schedulerEnabled.setValue(true);
          LX.log("Opening schedule file: " + projectFile);
          lx.scheduler.openSchedule(projectFile, true);
        } else {
          LX.log("Opening initial project file: " + projectFile);
          lx.openProject(projectFile);
        }
      }
    }
    lx.engine.start();
    // TODO: PLAY SOUND (if comfort zone)
    // TODO: START TIMER

    // Initialize control loop
    int i = 0;
    int nextFileNumber = 1;
    // Replace with second .lxp file for testing
    File projectFile2 = new File(System.getProperty("user.home") + "/git/pleasure-dairy/pleasure_dairy/lighting/scratch_pad/test-ring2.lxp");

    // Control loop
    while(true) {
      // TODO: CHECK GPIO
      // TODO: CHECK TIMER
      if (i == 5) {
        // Move to next pattern
        if (nextFileNumber == 0) {
          lx.openProject(projectFile);
          nextFileNumber = 1;
        } else {
          lx.openProject(projectFile2);
          nextFileNumber = 0;
        }
        i = 0;
      } else {
        try {
          Thread.sleep(1000);
          LX.log("test" + i);
        } catch (InterruptedException e) {
          e.printStackTrace();
        }
        i = i + 1;
      }
    }
  }

  /**
   * Main interface into the program. Two modes are supported, if the --headless
   * flag is supplied then a raw CLI version of LX is used. If not, then we embed
   * in a Processing 4 applet and run as such.
   *
   * @param args Command-line arguments
   */
  public static void main(String[] args) {
    LX.log("Initializing LX version " + LXStudio.VERSION);
    LX.log("Running java " +
      System.getProperty("java.version") + " " +
      System.getProperty("java.vendor") + " " +
      System.getProperty("os.name") + " " +
      System.getProperty("os.version") + " " +
      System.getProperty("os.arch")
    );
    boolean headless = false;
    File projectFile = null;
    for (int i = 0; i < args.length; ++i) {
      if ("--help".equals(args[i])) {
      } else if ("--headless".equals(args[i])) {
        headless = true;
      } else if ("--fullscreen".equals(args[i]) || "-f".equals(args[i])) {
        FULLSCREEN = true;
      } else if ("--width".equals(args[i]) || "-w".equals(args[i])) {
        try {
          WIDTH = Integer.parseInt(args[++i]);
        } catch (Exception x ) {
          LX.error("Width command-line argument must be followed by integer");
        }
      } else if ("--height".equals(args[i]) || "-h".equals(args[i])) {
        try {
          HEIGHT = Integer.parseInt(args[++i]);
        } catch (Exception x ) {
          LX.error("Height command-line argument must be followed by integer");
        }
      } else if ("--windowx".equals(args[i]) || "-x".equals(args[i])) {
        try {
          WINDOW_X = Integer.parseInt(args[++i]);
          HAS_WINDOW_POSITION = true;
        } catch (Exception x ) {
          LX.error("Window X command-line argument must be followed by integer");
        }
      } else if ("--windowy".equals(args[i]) || "-y".equals(args[i])) {
        try {
          WINDOW_Y = Integer.parseInt(args[++i]);
          HAS_WINDOW_POSITION = true;
        } catch (Exception x ) {
          LX.error("Window Y command-line argument must be followed by integer");
        }
      } else if (args[i].endsWith(".lxp")) {
        try {
          projectFile = new File(args[i]);
        } catch (Exception x) {
          LX.error(x, "Command-line project file path invalid: " + args[i]);
        }
      }
    }
    if (headless) {
      // We're not actually going to run this as a PApplet, but we need to explicitly
      // construct and set the initialize callback so that any custom components
      // will be run
      LX.Flags flags = new LX.Flags();
      flags.initialize = new LXStudioApp();
      if (projectFile == null) {
        LX.log("WARNING: No project filename was specified for headless mode!");
      }
      pdHeadless(flags, projectFile);
    } else {
      PApplet.main("heronarts.lx.app.LXStudioApp", args);
    }
  }

}

