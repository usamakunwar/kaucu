module.exports = function(grunt) {
    grunt.initConfig({
      terser: {
        options: {},
        build: {
          files: {
            'kaucu/static/js/build.js': 
            [
            'bower_components/jquery/dist/jquery.js',
            'bower_components/bootstrap/dist/js/bootstrap.bundle.js',
            'bower_components/typeahead.js/dist/typeahead.bundle.js',
            'bower_components/bootstrap-select/dist/js/bootstrap-select.js', 
            ]
          }
        },
        cust: {
          files: {
            'kaucu/static/js/common.js': ['src/javascripts/common.js'],
            'kaucu/static/js/form.js': ['src/javascripts/form.js'],
            'kaucu/static/js/chart.js': ['bower_components/chart.js/dist/Chart.js'],
          }
        } 
      },
      cssmin: {
        options: {},
        target: {
          files: {
            'kaucu/static/css/build.css':
            [
            'bower_components/bootstrap/dist/css/bootstrap.css', 
            'bower_components/bootstrap-select/dist/css/bootstrap-select.css', 
            'bower_components/fontawesome/css/all.css', 
            'src/stylesheets/style.css',
            ]
          }
        }
      },
      watch: {
        js: {
          files: ['src/javascripts/*.js'],
          tasks: ['terser:cust']
        },
        css: {
          files: ['src/stylesheets/*.css'],
          tasks: ['cssmin']
        },
      },
    });
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-terser');
    grunt.loadNpmTasks('grunt-contrib-watch');


    //grunt.registerTask('default', ['uglify','concat', 'apple']);
  
  };