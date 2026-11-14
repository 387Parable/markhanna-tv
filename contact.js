module.exports=async function(req,res){
 if(req.method!=='POST') return res.status(405).json({message:'Use the contact form to send a message.'});
 const {firstName,lastName,email,message,website}=req.body||{};
 if(website) return res.status(400).json({message:'The message could not be accepted.'});
 if([firstName,lastName,email,message].some(v=>typeof v!=='string'||!v.trim())||firstName.length>100||lastName.length>100||email.length>254||message.length>5000||!/^\S+@[^\s@]+\.[^\s@]+$/.test(email))
  return res.status(400).json({message:'Please check the required fields.'});
 const {RESEND_API_KEY,CONTACT_FROM,CONTACT_TO}=process.env;
 if(!RESEND_API_KEY||!CONTACT_FROM||!CONTACT_TO) return res.status(503).json({message:'Contact delivery is not connected on this preview.'});
 try{
  const upstream=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:'Bearer '+RESEND_API_KEY,'Content-Type':'application/json'},body:JSON.stringify({from:CONTACT_FROM,to:[CONTACT_TO],reply_to:email,subject:'Mark Hanna website inquiry',text:firstName+' '+lastName+'\n'+email+'\n\n'+message})});
  if(upstream.ok) return res.status(200).json({message:'Thank you. Your message has been sent.'});
 }catch{}
 return res.status(502).json({message:'Your message could not be sent. Please try again.'});
};
