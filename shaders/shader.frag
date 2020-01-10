#version 330 core
//uniform float time;
uniform vec4 fvAmbient;
uniform vec4 fvSpecular;
uniform vec4 fvDiffuse;

uniform sampler2D baseMap;
uniform sampler2D bumpMap;

//in vec4 FragmentColor;
out vec4 FragColor;
//attribute vec2 Texcoord; // attribute only in vertex shader ALLOWED

varying vec2 tC; // in
varying vec3 ViewDirection;
varying vec3 LightDirection;
void main(){
    vec3  fvLightDirection = normalize( LightDirection );
    
    vec3  fvNormal         = normalize( ( texture2D( bumpMap, tC ).xyz * 2.0 ) - 1.0 );
    float fNDotL           = dot( fvNormal, fvLightDirection ); 

    vec3  fvReflection     = normalize( ( ( 2.0 * fvNormal ) * fNDotL ) - fvLightDirection ); 
    vec3  fvViewDirection  = normalize( ViewDirection );
    float fRDotV           = max( 0.0, dot( fvReflection, fvViewDirection ) );


    vec4  fvBaseColor      = texture2D( baseMap, tC );
    
    vec4  fvTotalAmbient   = fvAmbient * fvBaseColor; 
    vec4  fvTotalDiffuse   = fvDiffuse * fNDotL * fvBaseColor; 
    vec4  fvTotalSpecular  = fvSpecular * ( pow( fRDotV, 2.0 ) );
    
    gl_FragColor = fvTotalAmbient + fvTotalDiffuse + fvTotalSpecular;
}