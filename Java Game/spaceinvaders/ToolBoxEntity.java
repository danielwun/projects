package org.newdawn.spaceinvaders;

import java.lang.Math ;
/**
 * An entity representing a shot fired by the player's ship
 * 
 * @author Kevin Glass
 */
public class ToolBoxEntity extends Entity {
	/** The vertical speed at which the players shot moves */
	private double moveSpeed = 100;
	/** The game in which this entity exists */
	private Game game;
	/** True if this shot has been "used", i.e. its hit something */
	private boolean used = false;
	private int randomNumber = 0 ;
	private double time = 0 ;
	
	/**
	 * Create a new shot from the player
	 * 
	 * @param game The game in which the shot has been created
	 * @param sprite The sprite representing this shot
	 * @param x The initial x location of the shot
	 * @param y The initial y location of the shot
	 */
	public ToolBoxEntity(Game game,String sprite,int x,int y) {
		super(sprite,x,y);
		
		this.game = game;
		
		dy = moveSpeed;
	}
	// 紀錄道具出現的時間
	public void setTime(double time){}
	// 取得時間
	public double getTime(){
		return time ;
	} 
	public void delete(){}

	/**
	 * Request that this shot moved based on time elapsed
	 * 
	 * @param delta The time that has elapsed since last move
	 */
	public void move(long delta) {
		// proceed with normal move
		super.move(delta);
		
		// if we shot off the screen, remove ourselfs
		if (y > 800) {
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
		if (other instanceof ShipEntity ) {
			// remove the affected entities
			randomNumber= (int)( Math.random()*4)+1 ;
			game.creatTool( randomNumber) ;
			game.removeEntity(this);
		}
	}
}