#version 330 core
attribute vec3 vertexPosition;
//attribute vec4 vertexColor;    // _colorProgram.addAttribute("vertexColor");
attribute vec2 Texcoord;
attribute vec3 rm_Binormal;
attribute vec3 rm_Tangent;

//out vec4 FragmentColor;
varying vec2 tC; //out - to je ovo sta ide DALJE!
varying vec3 ViewDirection;
varying vec3 LightDirection;

//uniform float scaleAll;
uniform vec4 translateVector;
uniform float scale;
uniform vec3 fvLightPosition;
uniform vec3 fvEyePosition;
uniform vec4 rotate;

void main(){
    vec3 pos =  (vec3(gl_ModelViewMatrix * vec4(vertexPosition.x,vertexPosition.y,vertexPosition.z, 1.0)));

    //vec3 pos =  (vec3(gl_ModelViewMatrix * vec4(vertexPosition.x+translateVector.x,vertexPosition.y+translateVector.y,vertexPosition.z+translateVector.z, 1.0)));
    //TODO: da se light Pametno ponasa
    //vec3 pos =  vec3(vertexPosition.x+translateVector.x,vertexPosition.y+translateVector.y,vertexPosition.z+translateVector.z);

    vec3 Light = fvLightPosition - pos;
    vec3 Eye   = fvEyePosition - pos;

    vec3 Tangent = normalize(vec3(gl_NormalMatrix * rm_Tangent));
    //normala je obicno u koordinatnom sustavu objekta
    vec3 Normal = normalize(vec3(gl_NormalMatrix * gl_Normal));
    vec3 Binormal = normalize(vec3(gl_NormalMatrix * rm_Binormal));

    LightDirection.x = dot(Light, Tangent);
    LightDirection.y = dot(Light, Binormal);
    LightDirection.z = dot(Light, Normal);
    
    ViewDirection.x = dot(Eye, Tangent);
    ViewDirection.y = dot(Eye, Binormal);
    ViewDirection.z = dot(Eye, Normal);
    
    
    mat4 transformMatrix = mat4(
        vec4(1.0,0.0,0.0,0.0),
        vec4(0.0,1.0,0.0,0.0),
        vec4(0.0,0.0,1.0,0.0),
        vec4(translateVector.x,translateVector.y,translateVector.z,translateVector.w));//
    
    
    vec3 axis = normalize(rotate.xyz); //[0,0,0,0]
    float s = sin(rotate.w); // 0
    float c = cos(rotate.w); // 1
    float oc = 1.0-c; //0
    mat4 rotateMatrix = mat4(
        vec4(oc * axis.x * axis.x + c,           oc * axis.x * axis.y - axis.z * s,  oc * axis.z * axis.x + axis.y * s,  0.0),
        vec4(oc * axis.x * axis.y + axis.z * s,  oc * axis.y * axis.y + c,           oc * axis.y * axis.z - axis.x * s,  0.0),
        vec4(oc * axis.z * axis.x - axis.y * s,  oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c,           0.0),
        vec4(0.0,0.0,0.0,1.0));
    
    
    mat4 scaleMatrix = mat4(
        vec4(scale,0.0,0.0,0.0),
        vec4(0.0,scale,0.0,0.0),
        vec4(0.0,0.0,scale,0.0),
        vec4(0.0,0.0,0.0,1.0));

    vec4 final_position= transformMatrix*rotateMatrix*scaleMatrix*vec4(vertexPosition.x, vertexPosition.y, vertexPosition.z, 0.5);
    gl_Position = gl_ProjectionMatrix *gl_ModelViewMatrix *final_position;
    

    tC = Texcoord;
    
}