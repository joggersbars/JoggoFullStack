const http = require('http');
const fs = require('fs');
const path = require('path');

// Puerto del servidor
const port = 8001;

// Crear el servidor
http.createServer((req, res) => {
  // Ruta del archivo solicitado
  // MAQUINA DE ESTADOS SEGUN LA URL QUE SE SOLICITE
  let filePath = path.join(__dirname, 'public/Recursos', req.url === '/' ? 'index.html' : req.url);     //pagina inicial

  if (req.url === '/login') {
    filePath = path.join(__dirname, 'public/Recursos', 'login.html');
  } else if (req.url === '/games') {
    filePath = path.join(__dirname, 'public/Recursos', 'games.html');
  } else if (req.url === '/yonunca_intro') {
    filePath = path.join(__dirname, 'public/Recursos', 'yonunca_intro.html');
  } else if (req.url === '/intro_jugador') {
    filePath = path.join(__dirname, 'public/Recursos', 'intro_jugador.html');
  } else if (req.url === '/yonunca_game') {
    filePath = path.join(__dirname, 'public/Recursos', 'yonunca_game.html');
  } else if (req.url === '/yonunca_stats') {
    filePath = path.join(__dirname, 'public/Recursos', 'yonunca_stats.html');
  }else if (req.url === '/partida') {
    filePath = path.join(__dirname, 'public/Recursos', 'partida.html');
  }


  // Si es una solicitud para los archivos estáticos en "src" o "pruebas" (CSS, JS, imágenes)
  if (req.url.startsWith('/src/') || req.url.startsWith('/pruebas/')) {
    filePath = path.join(__dirname, req.url);  // Mantener la estructura original de "src" y "pruebas"
  }
   // Añadir un console.log para depuración
   console.log('Archivo solicitado:', filePath);  // Ver qué archivo está siendo solicitado

  // Extensión del archivo
  let extname = String(path.extname(filePath)).toLowerCase();
  
  // Tipos MIME para servir diferentes archivos
  const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.wav': 'audio/wav',
    '.mp4': 'video/mp4',
    '.woff': 'application/font-woff',
    '.ttf': 'application/font-ttf',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'application/font-otf',
    '.wasm': 'application/wasm'
  };

  // Determinar el tipo MIME del archivo solicitado
  let contentType = mimeTypes[extname] || 'application/octet-stream';

  // Leer el archivo y servirlo
  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === 'ENOENT') {
        // Archivo no encontrado, servir una página 404
        fs.readFile(path.join(__dirname, 'public', '404.html'), (err, content404) => {
          res.writeHead(404, { 'Content-Type': 'text/html' });
          res.end(content404, 'utf-8');
        });
      } else {
        // Error de servidor
        res.writeHead(500);
        res.end(`Error del servidor: ${error.code}`);
      }
    } else {
      // Servir el archivo solicitado
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
}).listen(port, () => {                                             //Iniciar el servidor
  console.log(`Servidor corriendo en http://localhost:${port}`);
});
