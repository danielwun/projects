package org.newdawn.spaceinvaders;

import java.lang.Math ;
import java.awt.Canvas;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics2D;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.BufferStrategy;
import java.util.ArrayList;

import javax.swing.JFrame;
import javax.swing.JPanel;

/**
 * The main hook of our game. This class with both act as a manager
 * for the display and central mediator for the game logic. 
 * 
 * Display management will consist of a loop that cycles round all
 * entities in the game asking them to move and then drawing them
 * in the appropriate place. With the help of an inner class it
 * will also allow the player to control the main ship.
 * 
 * As a mediator it will be informed when entities within our game
 * detect events (e.g. alient killed, played died) and will take
 * appropriate game actions.
 * 
 * @author Kevin Glass
 */
public class Game extends Canvas {
	/** The stragey that allows us to use accelerate page flipping */
	private BufferStrategy strategy;
	/** True if the game is currently "running", i.e. the game loop is looping */
	private boolean gameRunning = true;
	/** The list of all the entities that exist in our game */
	private ArrayList entities = new ArrayList();
	/** The list of entities that need to be removed from the game this loop */
	private ArrayList removeList = new ArrayList();
	/** The entity representing the player */
	private Entity ship;
	/** The speed at which the player's ship should move (pixels/sec) */
	private double moveSpeed = 300;
	/** The time at which last fired a shot */
	private long lastFire = 0;
	/** The time at which last fired a shot */
	private long lastFire2 = 0;
	/** The interval between our players shot (ms) */
	private long firingInterval = 500;
	/** The number of aliens left on the screen */
	private int alienCount;
	/** 怪獸出現的時間間隔 */
	private double monsterInterval = 300 ;
	private double lastTime = 0 ;
	/** 怪獸上次出現的時間 */
	private long lastMonster = 0 ;
	/** X座標 */
	private int locationX = 0 ;
	/** Y座標 */
	private int locationY = 0 ;
	/** Y座標 */
	private int rocketY = 0 ;
	/** X座標 */
	private int rocketX = 0 ;
	/** 擊敗的敵人數用於計算產生道具的擊殺敵人數 */
	private int deathAlien = 0 ;
	/** 得到道具箱的擊殺敵人數 */
	private double getTool = 10 ;
	/** 產生大魔王的擊殺數 */
	private double getBoss = 100 ;
	/** 擊敗的敵人數用於計算產生道具的擊殺敵人數 */
	private int deathAlien2 = 0 ;
	/** 道具持續時間 */
	private double toolTime =0 ;
	/** 道具是否銷毀 */
	private boolean delete = false ;
	/** 一個隨機的數字 */
	private int randomNumber = 0 ;
	/** 擊殺的敵人數用於顯示在螢幕上的 */	
	private int killedAlien = 0 ;
	/** 兩種武器 */	 
	private int[] weapon = { 100000 , 0 } ;
	/** 選擇第幾種武器 */	
	private int countWeapon = 0 ;
	/** 更換武器的時間 */	
	private double transfer = 0 ;
	/** The message to display which waiting for a key press */
	private String message = "";
	/** True if we're holding up game play until a key has been pressed */
	private boolean waitingForKeyPress = true;
	/** True if the left cursor key is currently pressed */
	private boolean leftPressed = false;
	/** True if the right cursor key is currently pressed */
	private boolean rightPressed = false;
	/** True if the up cursor key is currently pressed */
	private boolean upPressed = false;
	/** True if the down cursor key is currently pressed */
	private boolean downPressed = false;
	/** True if we are firing */
	private boolean firePressed = false;
	private boolean zPressed = false;
	private boolean xPressed = false;
	/** True if game logic needs to be applied this loop, normally as a result of a game event */
	private boolean logicRequiredThisLoop = false;
	 
	/**
	 * Construct our game and set it running.
	 */
	public Game() {
		// create a frame to contain our game
		JFrame container = new JFrame("Space Invaders 101");
		
		// get hold the content of the frame and set up the resolution of the game
		JPanel panel = (JPanel) container.getContentPane();
		panel.setPreferredSize(new Dimension(800,600));
		panel.setLayout(null);
		
		// setup our canvas size and put it into the content of the frame
		setBounds(0,0,800,600);
		panel.add(this);
		
		// Tell AWT not to bother repainting our canvas since we're
		// going to do that our self in accelerated mode
		setIgnoreRepaint(true);
		
		// finally make the window visible 
		container.pack();
		container.setResizable(false);
		container.setVisible(true);
		
		// add a listener to respond to the user closing the window. If they
		// do we'd like to exit the game
		container.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				System.exit(0);
			}
		});
		
		// add a key input system (defined below) to our canvas
		// so we can respond to key pressed
		addKeyListener(new KeyInputHandler());
		
		// request the focus so key events come to us
		requestFocus();

		// create the buffering strategy which will allow AWT
		// to manage our accelerated graphics
		createBufferStrategy(2);
		strategy = getBufferStrategy();
		
		// initialise the entities in our game so there's something
		// to see at startup
		initEntities();
	}
	
	/**
	 * Start a fresh game, this should clear out any old data and
	 * create a new set.
	 */
	private void startGame() {
		// clear out any existing entities and intialise a new set
		entities.clear();
		initEntities();
		killedAlien = 0 ;
		monsterInterval = 300 ;
		weapon[0]=10000 ;
		weapon[1]=0 ;
		deathAlien = 0 ;
		deathAlien2 = 0 ;
		getTool = 10 ;
	    getBoss = 100 ;
		// blank out any keyboard settings we might currently have
		leftPressed = false;
		rightPressed = false;
		upPressed = false;
		downPressed = false;
		firePressed = false;
	}
	
	/**
	 * Initialise the starting state of the entities (ship and aliens). Each
	 * entitiy will be added to the overall list of entities in the game.
	 */
	private void initEntities() {
		// create the player ship and place it roughly in the center of the screen
		ship = new ShipEntity(this,"sprites/ship.gif",370,550);
		entities.add(ship);
		
		// create a block of aliens (5 rows, by 12 aliens, spaced evenly)
		
	}
	
	//  實例化道具箱
	public void creatToolBox( ){
			locationX = (int)( Math.random()*800) ;
			Entity ToolBox = new ToolBoxEntity(this,"sprites/ToolBox.gif",locationX,0);
			entities.add(ToolBox);
	}
	
	// 實例化道具
	public void creatTool( int number ){			
			//撞到道具箱的時候會產生一個亂碼，藉而挑選出一個道具
			
			//亂碼 1 代表 
			if( number == 1 ){
				ToolEntity Tool = new ToolEntity(this,"sprites/rocket.gif", ship.getX() , ship.getY() );
				entities.add(Tool);
			}else if( number == 2 ){
				BrickEntity Brick = new BrickEntity(this,"sprites/brick.gif", ship.getX() , ship.getY()-30 );
				entities.add(Brick);
			}else if( number == 3 ){
				weapon[0] = weapon[0] + 500 ;				
				if( weapon[0]>10000 ){
					weapon[0] = 10000 ;
				}	
			}else if( number == 4 ){
				weapon[1] = weapon[1] + 50 ;				
				if( weapon[1]>1000 ){
					weapon[1] = 1000 ;
				}	
			}
	}

	/**
	 * Notification from a game entity that the logic of the game
	 * should be run at the next opportunity (normally as a result of some
	 * game event)
	 */
	public void updateLogic() {
		logicRequiredThisLoop = true;
	}
	/*public void setEntities( Entity bossShot ){
		entities.add(bossShot) ;
	}*/
	public void setBossShot( int x ){
		BossShotEntity bossShot = new BossShotEntity(this,"sprites/shot.gif",x,0);
		entities.add(bossShot) ;
	}
	/**
	 * Remove an entity from the game. The entity removed will
	 * no longer move or be drawn.
	 * 
	 * @param entity The entity that should be removed
	 */
	public void removeEntity(Entity entity) {
		removeList.add(entity);
	}
	
	/**
	 * Notification that the player has died. 
	 */
	public void notifyDeath() {
		message = "Oh no! They got you, try again?";
		waitingForKeyPress = true;
	}
	public void killAlien(){
		killedAlien ++ ;
	}
	/**
	 * Notification that the player has won
 since all the aliens
	 * are dead.
	 */
	public void notifyWin() {
		message = "Well done! You Win!";
		waitingForKeyPress = true;
	}
	
	/**
	 * Notification that an alien has been killed
	 */
	public void notifyAlienKilled() {
		// reduce the alient count, if there are none left, the player has won!
		alienCount--;
		
		if (alienCount == 0) {
			notifyWin();
		}
		deathAlien ++ ;
		deathAlien2 ++ ;
		// if there are still some aliens left then they all need to get faster, so
		// speed up all the existing aliens
		for (int i=0;i<entities.size();i++) {
			Entity entity = (Entity) entities.get(i);
			
			if (entity instanceof AlienEntity) {
				// speed up by 2%
				entity.setHorizontalMovement(entity.getHorizontalMovement() * 1.02);
			}
		}
	}
	
	/**
	 * Attempt to fire a shot from the player. Its called "try"
	 * since we must first check that the player can fire at this 
	 * point, i.e. has he/she waited long enough between shots
	 */
	public void tryToFire() {
		// check that we have waiting long enough to fire
		
		if ( weapon[0] != 0 && countWeapon == 0 ) {
			if (System.currentTimeMillis() - lastFire < firingInterval ) {
				return;
			}
			// if we waited long enough, create the shot entity, and record the time.
			lastFire = System.currentTimeMillis();
			weapon[0]-- ;
			ShotEntity shot = new ShotEntity(this,"sprites/shot.gif",ship.getX()+10,ship.getY()-30);
			entities.add(shot);
		}else if ( weapon[1] != 0 && countWeapon == 1 ) {
			if (System.currentTimeMillis() - lastFire < firingInterval ) {
				return;
			}
			// if we waited long enough, create the shot entity, and record the time.
			lastFire = System.currentTimeMillis();
			weapon[1]-- ;
			RocketEntity rocket = new RocketEntity(this,"sprites/rocket2.gif",ship.getX()+10,ship.getY()-30);
			entities.add(rocket);
		}else{
			return ;
		}
		
	}
	// 輸入爆炸時的時間
	public void bombTime( double bombTime ){
			bombTime = toolTime ;
	}
	// 輸入火箭炮的座標Y	
	public void BombY( int y ){
		rocketY = y ;
	} 

	// 輸入火箭炮的座標X	
	public void BombX( int x ){
		rocketX = x ;
	}

	// 製造爆炸
	public void creatBomb(){
		Entity bomb = new BombEntity(this,"sprites/bomb.gif", rocketX , rocketY-20 );
		entities.add(bomb);
	}
	// 取得爆炸時的時間
	public void getTime( double bombTime ){
		toolTime = bombTime ;
	}
	/**
	 * The main game loop. This loop is running during all game
	 * play as is responsible for the following activities:
	 * <p>
	 * - Working out the speed of the game loop to update moves
	 * - Moving the game entities
	 * - Drawing the screen contents (entities, text)
	 * - Updating game events
	 * - Checking Input
	 * <p>
	 */
	public void gameLoop() {
		long lastLoopTime = System.currentTimeMillis();
		
		// keep looping round til the game ends
		while (gameRunning) {
			// work out how long its been since the last update, this
			// will be used to calculate how far the entities should
			// move this loop
			long delta = System.currentTimeMillis() - lastLoopTime;
			lastLoopTime = System.currentTimeMillis();
			
			// Get hold of a graphics context for the accelerated 
			// surface and blank it out
			Graphics2D g = (Graphics2D) strategy.getDrawGraphics();
			g.setColor(Color.black);
			g.fillRect(0,0,800,600);
			if( System.currentTimeMillis() - lastTime > 100 ){
				monsterInterval = monsterInterval * 0.9999 ;
				lastTime = System.currentTimeMillis() ;
			}
			// 敵人死亡數大於獲得道具的規定數量時，跑出道具箱
			if( deathAlien >= getTool ){
				creatToolBox() ;
				deathAlien = 0 ;
				getTool = getTool* 1.02 ;
			}
			
			// 假如遊戲開始，敵人開始出現
			if (!waitingForKeyPress){
				if( System.currentTimeMillis() - lastMonster > monsterInterval ){
					lastMonster = System.currentTimeMillis() ;
					locationX = (int)( Math.random()*800) ;
					Entity alien = new AlienEntity(this,"sprites/alien.gif",locationX,0);
					entities.add(alien);
				}
			}

			// 爆炸時間控制
			if( System.currentTimeMillis() -toolTime > 100 ){
				delete = true ;
			}

			for (int i=0;i<entities.size();i++) {
				Entity entity = (Entity) entities.get(i);
				if( entity instanceof AlienEntity){
					if( ( entity.getX() > ship.getX() ) && entity.getHorizontalMovement()>0 ){
							entity.doLogic() ;
					}
					if( ( entity.getX() < ship.getX() ) && entity.getHorizontalMovement()<0 ){
							entity.doLogic() ;
					}
				}
				if( entity instanceof BombEntity ){
					if( System.currentTimeMillis() - entity.getTime() > 150 ){
						entity.delete() ;
						//delete = false ;
					}
				}
				if( entity instanceof BossEntity ){
					locationX = entity.getX() ;
					entity.setTime( System.currentTimeMillis() ) ;
				}
			}
			
			// 敵人死亡數大於一定數量，跑出大魔王
			if( deathAlien2 >= getBoss ){
				Entity boss = new BossEntity(this,"sprites/alien(1).gif",locationX,50);
				entities.add(boss);
				deathAlien2 = 0 ;
				getBoss = getBoss* 0.95 ;
				
			}
			// cycle round asking each entity to move itself
			if (!waitingForKeyPress) {
				for (int i=0;i<entities.size();i++) {
					Entity entity = (Entity) entities.get(i);
					entity.move(delta);
				}
			}
			// cycle round drawing all the entities we have in the game
			for (int i=0;i<entities.size();i++) {
				Entity entity = (Entity) entities.get(i);
				entity.draw(g);
			}
			
			// brute force collisions, compare every entity against
			// every other entity. If any of them collide notify 
			// both entities that the collision has occured
			for (int p=0;p<entities.size();p++) {
				for (int s=p+1;s<entities.size();s++) {
					Entity me = (Entity) entities.get(p);
					Entity him = (Entity) entities.get(s);
					
					if (me.collidesWith(him)) {
						me.collidedWith(him);
						him.collidedWith(me);
					}
				}
			}
			
			// remove any entity that has been marked for clear up
			entities.removeAll(removeList);
			removeList.clear();

			// if a game event has indicated that game logic should
			// be resolved, cycle round every entity requesting that
			// their personal logic should be considered.
			if (logicRequiredThisLoop) {
				for (int i=0;i<entities.size();i++) {
					Entity entity = (Entity) entities.get(i);
					entity.doLogic();
				}
				
				logicRequiredThisLoop = false;
			}
			
			// if we're waiting for an "any key" press then draw the 
			// current message 
			if (waitingForKeyPress) {
				g.setColor(Color.yellow);
				g.drawString(message,(800-g.getFontMetrics().stringWidth(message))/2,250);
				g.drawString("按任意鍵",(800-g.getFontMetrics().stringWidth("按任意鍵"))/2,300);
				g.drawString("原作品網址:www.CokeAndCode.com",10,15);
				g.drawString("Tutorial and Source written by Kevin Glass ",10,27);
				g.drawString("Game sprites provided by Ari Feldman ",10,39);
				g.drawString("A large number of people over at the Java Gaming Forums  ",10,51);
				g.drawString("改編者:葉尚畇、岳孝豐",10,63);
			}else{
				String s = Integer.toString(killedAlien); 
				g.setColor(Color.yellow);
				g.drawString(s,(800-g.getFontMetrics().stringWidth(s))/2,100);
				g.drawString(s,(800-g.getFontMetrics().stringWidth(s))/2,100);
				String str = Integer.toString(weapon[countWeapon]);
				g.drawString(str,ship.getX(),ship.getY()-5);
				g.drawString(str,ship.getX(),ship.getY()-5);
			}
			// finally, we've completed drawing so clear up the graphics
			// and flip the buffer over
			g.dispose();
			strategy.show();
			
			// resolve the movement of the ship. First assume the ship 
			// isn't moving. If either cursor key is pressed then
			// update the movement appropraitely
			ship.setHorizontalMovement(0);
			ship.setVerticalMovement(0);
			if ((leftPressed) && (!rightPressed)) {
				ship.setHorizontalMovement(-moveSpeed);
			} else if ((rightPressed) && (!leftPressed)) {
				ship.setHorizontalMovement(moveSpeed);
			} else if ((upPressed) && (!downPressed)) {
				ship.setVerticalMovement(-moveSpeed);
			} else if ((downPressed) && (!upPressed)) {
				ship.setVerticalMovement(moveSpeed);
			}
			
			// if we're pressing fire, attempt to fire
			if (firePressed) {
				tryToFire();
			}
			if ( zPressed && ((System.currentTimeMillis() - transfer)>200) ) {
				transfer = System.currentTimeMillis() ;
				if(countWeapon == 0){
					countWeapon = 1 ;
				}else{
					countWeapon-- ;
				 }
				
			}
			if ( xPressed && ((System.currentTimeMillis() - transfer)>200)  ) {
				transfer = System.currentTimeMillis() ;
				if(countWeapon==1){
					countWeapon = 0 ;
				}else{
					countWeapon++ ;
				 }
			}
			
			// finally pause for a bit. Note: this should run us at about
			// 100 fps but on windows this might vary each loop due to
			// a bad implementation of timer
			try { Thread.sleep(10); } catch (Exception e) {}
		}
	}
	
	/**
	 * A class to handle keyboard input from the user. The class
	 * handles both dynamic input during game play, i.e. left/right 
	 * and shoot, and more static type input (i.e. press any key to
	 * continue)
	 * 
	 * This has been implemented as an inner class more through 
	 * habbit then anything else. Its perfectly normal to implement
	 * this as seperate class if slight less convienient.
	 * 
	 * @author Kevin Glass
	 */
	private class KeyInputHandler extends KeyAdapter {
		/** The number of key presses we've had while waiting for an "any key" press */
		private int pressCount = 1;
		
		/**
		 * Notification from AWT that a key has been pressed. Note that
		 * a key being pressed is equal to being pushed down but *NOT*
		 * released. Thats where keyTyped() comes in.
		 *
		 * @param e The details of the key that was pressed 
		 */
		public void keyPressed(KeyEvent e) {
			// if we're waiting for an "any key" typed then we don't 
			// want to do anything with just a "press"
			if (waitingForKeyPress) {
				return;
			}
			
			
			if (e.getKeyCode() == KeyEvent.VK_LEFT) {
				leftPressed = true;
			}
			if (e.getKeyCode() == KeyEvent.VK_RIGHT) {
				rightPressed = true;
			}
			if (e.getKeyCode() == KeyEvent.VK_UP) {
				upPressed = true;
			}
			if (e.getKeyCode() == KeyEvent.VK_Z) {
				zPressed = true;
			}
			if (e.getKeyCode() == KeyEvent.VK_X) {
				xPressed = true;
			}
			if (e.getKeyCode() == KeyEvent.VK_DOWN) {
				downPressed = true;
			}
			if (e.getKeyCode() == KeyEvent.VK_SPACE) {
				firePressed = true;
			}
		} 
		
		/**
		 * Notification from AWT that a key has been released.
		 *
		 * @param e The details of the key that was released 
		 */
		public void keyReleased(KeyEvent e) {
			// if we're waiting for an "any key" typed then we don't 
			// want to do anything with just a "released"
			if (waitingForKeyPress) {
				return;
			}
			
			if (e.getKeyCode() == KeyEvent.VK_LEFT) {
				leftPressed = false;
			}
			if (e.getKeyCode() == KeyEvent.VK_RIGHT) {
				rightPressed = false;
			}
			if (e.getKeyCode() == KeyEvent.VK_UP) {
				upPressed = false;
			}
			if (e.getKeyCode() == KeyEvent.VK_X) {
				xPressed = false;
			}
			if (e.getKeyCode() == KeyEvent.VK_Z) {
				zPressed = false;
			}
			if (e.getKeyCode() == KeyEvent.VK_DOWN) {
				downPressed = false ;
			}
			if (e.getKeyCode() == KeyEvent.VK_SPACE) {
				firePressed = false;
			}
		}

		/**
		 * Notification from AWT that a key has been typed. Note that
		 * typing a key means to both press and then release it.
		 *
		 * @param e The details of the key that was typed. 
		 */
		public void keyTyped(KeyEvent e) {
			// if we're waiting for a "any key" type then
			// check if we've recieved any recently. We may
			// have had a keyType() event from the user releasing
			// the shoot or move keys, hence the use of the "pressCount"
			// counter.
			if (waitingForKeyPress) {
				if (pressCount == 1) {
					// since we've now recieved our key typed
					// event we can mark it as such and start 
					// our new game
					waitingForKeyPress = false;
					startGame();
					pressCount = 0;
				} else {
					pressCount++;
				}
			}
			
			// if we hit escape, then quit the game
			if (e.getKeyChar() == 27) {
				System.exit(0);
			}
		}
	}
	
	/**
	 * The entry point into the game. We'll simply create an
	 * instance of class which will start the display and game
	 * loop.
	 * 
	 * @param argv The arguments that are passed into our game
	 */
	public static void main(String argv[]) {
		Game g =new Game();

		// Start the main game loop, note: this method will not
		// return until the game has finished running. Hence we are
		// using the actual main thread to run the game.
		g.gameLoop();
	}
}
