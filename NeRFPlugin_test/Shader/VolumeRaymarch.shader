Shader "NeRFPlugin/VolumeRaymarch"
{
    Properties
    {
        _VolumeTex ("Volume Texture", 3D) = "" {}
        _StepSize ("Step Size", Float) = 0.005
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        Pass
        {
            ZWrite Off
            Cull Off
            Blend SrcAlpha OneMinusSrcAlpha

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"

            sampler3D _VolumeTex;
            float _StepSize;

            struct appdata
            {
                float4 vertex : POSITION;
                float3 uv : TEXCOORD0;
            };

            struct v2f
            {
                float4 vertex : SV_POSITION;
                float3 worldPos : TEXCOORD0;
            };

            v2f vert(appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
                return o;
            }

            float4 frag(v2f i) : SV_Target
            {
                float3 rayDir = normalize(i.worldPos - _WorldSpaceCameraPos);
                float3 rayOrigin = i.worldPos;

                float3 boxMin = float3(-0.5, -0.5, -0.5);
                float3 boxMax = float3(0.5, 0.5, 0.5);

                float3 t0 = (boxMin - rayOrigin) / rayDir;
                float3 t1 = (boxMax - rayOrigin) / rayDir;

                float3 tmin = min(t0, t1);
                float3 tmax = max(t0, t1);

                float tNear = max(max(tmin.x, tmin.y), tmin.z);
                float tFar = min(min(tmax.x, tmax.y), tmax.z);

                if (tNear > tFar || tFar < 0) return float4(0,0,0,0);

                float sum = 0;
                float steps = 0;
                for (float t = tNear; t < tFar; t += _StepSize)
                {
                    float3 pos = rayOrigin + t * rayDir;
                    float3 uvw = pos + 0.5;
                    float d = tex3D(_VolumeTex, uvw).r;
                    sum += d;
                    steps++;
                }

                float alpha = saturate(sum / steps);
                return float4(alpha, alpha, alpha, alpha);
            }
            ENDCG
        }
    }
}
