package org.newdawn.spaceinvaders;

/**
 * An entity representing a shot fired by the player's ship
 * 
 * @author Kevin Glass
 */
public class RocketEntity extends Entity {
	/** The vertical speed at which the players shot moves */
	private double moveSpeed = -400;
	/** The game in which this entity exists */
	private Game game;
	private double time = 0 ;
	/** True if this shot has been "used", i.e. its hit something */
	
	/**
	 * Create a new shot from the player
	 * 
	 * @param game The game in which the shot has been created
	 * @param sprite The sprite representing this shot
	 * @param x The initial x location of the shot
	 * @param y The initial y location of the shot
	 */
	public RocketEntity(Game game,String sprite,int x,int y) {
		super(sprite,x,y);
		
		this.game = game;
		
		dy = moveSpeed;
	}
	// 紀錄時間
	public void setTime( double time ){	}
	public void delete(){}
	// 取得時間
	public double getTime(){
		return time ;
	} 
	/**
	 * Request that this shot moved based on time elapsed
	 * 
	 * @param delta The time that has elapsed since last move
	 */
	public void move(long delta) {
		// proceed with normal move
		super.move(delta);
		
		// if we shot off the screen, remove ourselfs
		if (y < -100) {
			game.removeEntity(this);
		}
	}
	
	/**
	 * Notification that this shot has collided with another
	 * entity
	 * 
	 * @parma other The other entity with which we've collided
	 */
	public void collidedWith(Entity other) {
		// if we've hit an alien, kill it!
		if (other instanceof AlienEntity) {
			// 刪除火箭炮
			game.removeEntity(this);
			game.getTime( System.currentTimeMillis() ) ;
			game.BombY( this.getY()) ;
			game.BombX( this.getX()) ;
			game.creatBomb() ;
		}
	}
}