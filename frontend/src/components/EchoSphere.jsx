import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

const vertexShader = `
varying vec2 vUv;
varying float vDisplacement;
varying vec3 vNormal;
varying vec3 vViewPosition;

uniform float uTime;
uniform float uEnergy;
uniform float uEntropy;
uniform float uBreath;
uniform float uHeartbeat;

// Simplex noise function (simplified)
vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec4 permute(vec4 x) { return mod289(((x*34.0)+1.0)*x); }
vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }
float snoise(vec3 v) {
  const vec2  C = vec2(1.0/6.0, 1.0/3.0) ;
  const vec4  D = vec4(0.0, 0.5, 1.0, 2.0);
  vec3 i  = floor(v + dot(v, C.yyy) );
  vec3 x0 = v - i + dot(i, C.xxx) ;
  vec3 g = step(x0.yzx, x0.xyz);
  vec3 l = 1.0 - g;
  vec3 i1 = min( g.xyz, l.zxy );
  vec3 i2 = max( g.xyz, l.zxy );
  vec3 x1 = x0 - i1 + C.xxx;
  vec3 x2 = x0 - i2 + C.yyy;
  vec3 x3 = x0 - D.yyy;
  i = mod289(i);
  vec4 p = permute( permute( permute(
             i.z + vec4(0.0, i1.z, i2.z, 1.0 ))
           + i.y + vec4(0.0, i1.y, i2.y, 1.0 ))
           + i.x + vec4(0.0, i1.x, i2.x, 1.0 ));
  float n_ = 0.142857142857;
  vec3  ns = n_ * D.wyz - D.xzx;
  vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
  vec4 x_ = floor(j * ns.z);
  vec4 y_ = floor(j - 7.0 * x_ );
  vec4 x = x_ *ns.x + ns.yyyy;
  vec4 y = y_ *ns.x + ns.yyyy;
  vec4 h = 1.0 - abs(x) - abs(y);
  vec4 b0 = vec4( x.xy, y.xy );
  vec4 b1 = vec4( x.zw, y.zw );
  vec4 s0 = floor(b0)*2.0 + 1.0;
  vec4 s1 = floor(b1)*2.0 + 1.0;
  vec4 sh = -step(h, vec4(0.0));
  vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy ;
  vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww ;
  vec3 p0 = vec3(a0.xy,h.x);
  vec3 p1 = vec3(a0.zw,h.y);
  vec3 p2 = vec3(a1.xy,h.z);
  vec3 p3 = vec3(a1.zw,h.w);
  vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2, p2), dot(p3,p3)));
  p0 *= norm.x;
  p1 *= norm.y;
  p2 *= norm.z;
  p3 *= norm.w;
  vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
  m = m * m;
  return 42.0 * dot( m*m, vec4( dot(p0,x0), dot(p1,x1),
                                dot(p2,x2), dot(p3,x3) ) );
}

void main() {
  vUv = uv;
  vNormal = normalize(normalMatrix * normal);
  
  // Organic movement: Noise + Breathing + Heartbeat
  float noise = snoise(position * (1.0 + uEntropy) + uTime * (0.2 + uEnergy * 0.5));
  float breath = sin(uTime * 0.5) * uBreath;
  float heart = smoothstep(0.8, 1.0, sin(uTime * 4.0)) * uHeartbeat; // Sharp pulse
  
  vDisplacement = noise + breath + heart;
  
  vec3 newPosition = position + normal * (noise * (0.1 + uEnergy * 0.2) + breath + heart);
  
  vec4 mvPosition = modelViewMatrix * vec4(newPosition, 1.0);
  vViewPosition = -mvPosition.xyz;
  gl_Position = projectionMatrix * mvPosition;
}
`;

const fragmentShader = `
varying vec2 vUv;
varying float vDisplacement;
varying vec3 vNormal;
varying vec3 vViewPosition;

uniform float uTime;
uniform vec3 uResonance;
uniform float uEnergy;
uniform float uEntropy;

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main() {
  // Base color from resonance
  vec3 color = uResonance;
  
  // Subsurface Scattering Simulation (Fake)
  // Light wraps around the object
  vec3 viewDir = normalize(vViewPosition);
  vec3 normal = normalize(vNormal);
  float fresnel = pow(1.0 - dot(viewDir, normal), 3.0);
  
  // Core glow (inner energy)
  vec3 coreGlow = vec3(1.0, 0.8, 0.6) * (uEnergy * 0.5);
  
  // Surface ripples
  float ripple = sin(vDisplacement * 10.0 + uTime) * 0.1;
  
  // Quantum Decoherence (Static Noise)
  // Higher entropy = more visual static/interference
  float staticNoise = random(vUv * uTime) * uEntropy * 0.8;
  
  // Combine
  color += coreGlow * (0.5 - vDisplacement); // Deeper parts glow more
  color += fresnel * vec3(0.5, 0.8, 1.0) * 0.5; // Rim light
  color += ripple;
  color += vec3(staticNoise); // Add quantum noise
  
  // Pulse intensity
  float pulse = sin(uTime * (1.0 + uEnergy * 5.0)) * 0.1 + 0.9;
  color *= pulse;
  
  gl_FragColor = vec4(color, 0.95);
}
`;

const EchoSphere = ({ quantumState }) => {
    const mesh = useRef();

    const uniforms = useMemo(
        () => ({
            uTime: { value: 0 },
            uEnergy: { value: 0.5 },
            uEntropy: { value: 0.1 },
            uResonance: { value: new THREE.Vector3(0.5, 0.8, 1.0) },
            uBreath: { value: 0.05 },
            uHeartbeat: { value: 0.02 },
        }),
        []
    );

    useFrame((state) => {
        if (mesh.current) {
            const time = state.clock.getElapsedTime();
            mesh.current.material.uniforms.uTime.value = time;

            // Smoothly interpolate towards target values
            mesh.current.material.uniforms.uEnergy.value = THREE.MathUtils.lerp(
                mesh.current.material.uniforms.uEnergy.value,
                quantumState.energy || 0.5,
                0.05
            );
            mesh.current.material.uniforms.uEntropy.value = THREE.MathUtils.lerp(
                mesh.current.material.uniforms.uEntropy.value,
                quantumState.entropy || 0.1,
                0.05
            );

            const targetColor = new THREE.Vector3(
                quantumState.resonance?.[0] ?? 0.5,
                quantumState.resonance?.[1] ?? 0.8,
                quantumState.resonance?.[2] ?? 1.0
            );
            mesh.current.material.uniforms.uResonance.value.lerp(targetColor, 0.05);

            // Dynamic Biology Parameters based on state
            // High energy = faster breath, stronger heart
            const energy = mesh.current.material.uniforms.uEnergy.value;
            mesh.current.material.uniforms.uBreath.value = 0.05 + energy * 0.05;
            mesh.current.material.uniforms.uHeartbeat.value = 0.02 + energy * 0.08;

            // Rotate slowly
            mesh.current.rotation.y += 0.002;
            mesh.current.rotation.z = Math.sin(time * 0.2) * 0.1; // Slight floating tilt
        }
    });

    return (
        <mesh ref={mesh}>
            <icosahedronGeometry args={[2, 128]} /> {/* Higher detail for displacement */}
            <shaderMaterial
                vertexShader={vertexShader}
                fragmentShader={fragmentShader}
                uniforms={uniforms}
                transparent
                wireframe={false}
            />
        </mesh>
    );
};

export default EchoSphere;
