using UnityEngine;
using System.Collections;

public class Particles : MonoBehaviour {

	// Use this for initialization
	void Start () {
	}
	
	// Update is called once per frame
	void Update () {
		Color[] colours = { Color.red, Color.green, Color.blue, Color.cyan, Color.magenta, Color.yellow, Color.white };
		gameObject.particleSystem.startColor = colours[Random.Range (0, colours.Length)];
	}
}
