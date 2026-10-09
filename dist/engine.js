/* Original activation inspection / maximization. Network weights remain fixed during dreaming. */
(function(root){
const presets={texture:{name:'纹理回声',layer:'conv_pw_5_relu'},structure:{name:'形态漫游',layer:'conv_pw_11_relu'}};
function extractor(tf,base,key){return tf.model({inputs:base.inputs,outputs:base.getLayer(presets[key]?.layer||key).output});}
function objective(y,channel){return channel===null||channel===undefined?y.mean():y.slice([0,0,0,channel],[-1,-1,-1,1]).mean();}
function step(tf,model,x,rate,channel=null){return tf.tidy(()=>{const gradient=tf.grad(v=>objective(model.apply(v,{training:false}),channel))(x);return x.add(gradient.div(gradient.square().mean().sqrt().add(1e-8)).mul(rate)).clipByValue(-1,1);});}
async function inspect(tf,model,x){const t=tf.tidy(()=>model.predict(x).squeeze([0]));try{return{shape:t.shape,data:Array.from(await t.data())};}finally{t.dispose();}}
function map(activation,channel){const[h,w,c]=activation.shape,data=new Float32Array(h*w);let min=Infinity,max=-Infinity;for(let i=0;i<data.length;i++){data[i]=activation.data[i*c+channel];min=Math.min(min,data[i]);max=Math.max(max,data[i]);}return{width:w,height:h,data,min,max};}
function colors(m,range){const[min,max]=range||[m.min,m.max],rgba=new Uint8ClampedArray(m.data.length*4);for(let i=0;i<m.data.length;i++){const t=max===min?0:Math.max(0,Math.min(1,(m.data[i]-min)/(max-min)));rgba.set([Math.round(22+220*t),Math.round(26+215*Math.sqrt(t)),Math.round(40+70*Math.sin(t*Math.PI)),255],i*4);}return rgba;}
root.DreamEngine={presets,extractor,step,inspect,map,colors};
})(typeof window==='undefined'?globalThis:window);
