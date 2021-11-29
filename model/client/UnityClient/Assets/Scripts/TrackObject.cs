﻿using UnityEngine;
using System.Collections;
 
[AddComponentMenu("Camera-Control/Mouse Orbit with zoom")]
public class TrackObject: MonoBehaviour {
    public float speed = -0.15f;
    public bool click = false;
    OrbitCamera camera;


    // Use this for initialization
    void Start () 
    {
      this.camera = GameObject.Find("CameraAnchor/OrbitCamera").GetComponent<OrbitCamera>();
    }

    void LateUpdate () 
    {
        if (Input.GetMouseButtonDown(1)) {
            click = true;
        }

        if (Input.GetMouseButtonUp(1)) {
            click = false;
        }

        if (click) {
            float distance = this.camera.distance;
            float x = 0.5f * Input.GetAxis("Mouse X") * speed * distance;
            float y = 0.5f * Input.GetAxis("Mouse Y") * speed * distance;

            Vector3 movement = new Vector3(x, 0, y);
            Vector3 target   = Camera.main.transform.TransformDirection(movement);
            target.y = 0.0f;

            this.transform.position = this.transform.position + target;
        }
    }
 
    public static float ClampAngle(float angle, float min, float max)
    {
        if (angle < -360F)
            angle += 360F;
        if (angle > 360F)
            angle -= 360F;
        return Mathf.Clamp(angle, min, max);
    }
}