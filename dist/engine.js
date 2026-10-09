/* Original implementation of activation maximization; TensorFlow.js Apache-2.0. */
(function(root){
const presets={texture:{name:'纹理回声',layer:'conv_pw_5_relu',description:'强化局部线条、色块与重复纹理'},structure:{name:'形态漫游',layer:'conv_pw_11_relu',description:'强化更深层的组合图案与局部结构'}};
function extractor(tf,base,key){return tf.model({inputs:base.inputs,outputs:base.getLayer(presets[key].layer).output});}
function step(tf,model,x,rate){return tf.tidy(()=>{const gradient=tf.grad(v=>model.apply(v,{training:false}).mean())(x);const norm=gradient.div(gradient.square().mean().sqrt().add(1e-8));return x.add(norm.mul(rate)).clipByValue(-1,1);});}
root.DreamEngine={presets,extractor,step};
})(typeof window==='undefined'?globalThis:window);
