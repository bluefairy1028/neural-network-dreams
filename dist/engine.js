/* Real fixed-network inference and pixel optimization. No simulated result frames. */
window.DreamEngine={
extract(tf,model,layer){return tf.model({inputs:model.inputs,outputs:model.getLayer(layer).output});},
step(tf,extractor,x,rate,channel){return tf.tidy(()=>{const grad=tf.grad(v=>extractor.apply(v,{training:false}).slice([0,0,0,channel],[-1,-1,-1,1]).mean())(x);return x.add(grad.div(grad.square().mean().sqrt().add(1e-8)).mul(rate)).clipByValue(-1,1);});},
map(activation,channel){const[h,w,c]=activation.shape,data=new Float32Array(h*w);let min=Infinity,max=-Infinity;for(let i=0;i<data.length;i++){data[i]=activation.data[i*c+channel];min=Math.min(min,data[i]);max=Math.max(max,data[i]);}return{width:w,height:h,data,min,max};},
colors(m){const out=new Uint8ClampedArray(m.data.length*4);for(let i=0;i<m.data.length;i++){const t=m.max===m.min?0:(m.data[i]-m.min)/(m.max-m.min);out.set([Math.round(21+207*t),Math.round(26+171*t),Math.round(34+108*t),255],i*4);}return out;}
};
