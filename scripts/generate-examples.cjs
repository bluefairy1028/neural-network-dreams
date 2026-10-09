const tf=require('@tensorflow/tfjs'),fs=require('fs'),path=require('path'),{PNG}=require('pngjs');
require('../dist/engine.js');
(async()=>{
await tf.setBackend('cpu');await tf.ready();
const json=JSON.parse(fs.readFileSync('dist/model/model.json'));
json.modelTopology.model_config.config.layers[0].config.batch_input_shape=[null,null,null,3];
fs.writeFileSync('dist/model/model.json',JSON.stringify(json));
const weights=Buffer.concat(json.weightsManifest.flatMap(g=>g.paths.map(p=>fs.readFileSync('dist/model/'+p))));
const base=await tf.loadLayersModel(tf.io.fromMemory({modelTopology:json.modelTopology,weightSpecs:json.weightsManifest.flatMap(g=>g.weights),weightData:weights.buffer.slice(weights.byteOffset,weights.byteOffset+weights.byteLength)}));
base.trainable=false;
const png=PNG.sync.read(fs.readFileSync('dist/examples/input.png'));
const rgb=new Float32Array(png.width*png.height*3);for(let i=0;i<png.width*png.height;i++)for(let c=0;c<3;c++)rgb[i*3+c]=png.data[i*4+c];
const initial=tf.tidy(()=>tf.image.resizeBilinear(tf.tensor3d(rgb,[png.height,png.width,3]),[256,256]).div(127.5).sub(1).expandDims());
async function save(x,file){const values=await x.data();const p=new PNG({width:256,height:256});for(let i=0;i<256*256;i++){for(let c=0;c<3;c++)p.data[i*4+c]=Math.round((values[i*3+c]+1)*127.5);p.data[i*4+3]=255;}fs.writeFileSync(file,PNG.sync.write(p));}
await save(initial,'dist/examples/original.png');
const records=[];
for(const key of Object.keys(DreamEngine.presets)){
 const model=DreamEngine.extractor(tf,base,key);let x=initial.clone();const frames=[];const start=Date.now();
 for(let i=0;i<=40;i++){
  if(i>0){const next=DreamEngine.step(tf,model,x,0.012);x.dispose();x=next;}
  if(i%2===0){const file=`examples/${key}-${i}.png`;await save(x,'dist/'+file);frames.push({step:i,url:file});}
  if(i%10===0)console.log(key,i,Math.round((Date.now()-start)/1000)+'s');
 }
 records.push({id:key,title:key==='texture'?'轨道之外 · 纹理回声':'轨道之外 · 形态漫游',preset:key,layer:DreamEngine.presets[key].layer,model:'MobileNet V1 · 0.25 · ImageNet',strength:'中',stepSize:0.012,iterations:40,width:256,height:256,createdAt:new Date().toISOString(),source:'NASA / Eileen Collins · Public domain, via scikit-image',filename:'astronaut.png',original:'examples/original.png',frames,elapsedMs:Date.now()-start,engine:'TensorFlow.js 4.22.0 / CPU',objective:'mean activation; gradient normalized by RMS; input clipped to [-1,1]',crop:false});x.dispose();
}
fs.writeFileSync('dist/examples/manifest.json',JSON.stringify(records,null,2));console.log('DONE');
})().catch(e=>{console.error(e);process.exit(1)});
