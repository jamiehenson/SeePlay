using UnityEngine;
using System.Collections;

public class Surface : MonoBehaviour 
{
	public Type SurfaceType;

	public enum Type 
	{
		Floor, Wall, SadWall
	}

	// Use this for initialization
	void Start () 
	{
		Color[] colours = { Color.red, Color.green, Color.yellow, Color.black, Color.white };

		if (SurfaceType == Type.Wall) 
		{
			gameObject.transform.renderer.material.color = colours[Random.Range (0,4)];
		}
		else if (SurfaceType == Type.SadWall)
		{
			gameObject.transform.renderer.material.color = Color.blue;
		}
	}
}
