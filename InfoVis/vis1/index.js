 var margin = {top: 15, right: 30, bottom: 90, left: 150},
    width = 1500 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;


// append the svg object to the body of the page
var svg = d3.select("#my_dataviz")
  .append("svg")
  .attr("fill-opacity",0.6)
    .attr("width", width + margin.left + margin.right+200)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");


 console.log(width + margin.left + margin.right+200);

    d3.csv("data.csv",function(dataa){
        
        function drawBar(y){

           
           
            var yr = y;

            var data = dataa.filter(function(d){
                if(d.year == yr){
                    return{
                        country : d.country,
                        count : d.count
                    }
                }
            });
            //console.log( data);

                    data.sort(function(a, b) {
                        return a.count - b.count;
                    });
                
                    console.log( data);
                    
                    var x = d3.scaleLinear()
                                .range([0, width])
                                .domain([0, d3.max(data, function (d) {
                                    return parseInt(d.count);

                                })]);
                
                var c = d3.max(data, function (d) {
                 
                        return d.count;
                    }); 
                        
                    
                
                var y = d3.scaleBand()
                            .rangeRound([height, 0])
                            .padding(0.1)
                            .domain(data.map(function (d) {
                              
                                    return d.country;
                                
                            }));
                
                var yAxis = d3.axisLeft()
                            .scale(y)
                            .tickSize(0);
                
                var gy = svg.append("g")
                            .attr("class", "y axis")
                            .call(yAxis)
                            .attr('fill', 'darkOrange');
                
                var bars = svg.selectAll(".bar")
                            .data(data)
                            .enter()
                            .append("g");
                            
                
                
                //append rects
                bars.append("rect")
                    .attr("class", "bar")
                    .attr("y", function (d) {
                       
                            return y(d.country);
                        
                    })
                    .attr("height", y.bandwidth())
                    .attr("x", 0)
                    .transition().duration(500).ease(d3.easeLinear).attr("width",function(d){
                        
                        return x(d.count);
                        
                    });
                
                
                //add a value label to the right of each bar
                bars.append("text")
                    .attr("class", "label")
                    //.transition().duration(50)
                    //y position of the label is halfway down the bar
                    .attr("y", function (d) {
                       
                        return y(d.country) + y.bandwidth() / 2 + 4;
                        
                    })
                    .attr("x",function (d) {
                        
                        return x(d.country) + 3;
                        
                    })
                    .text(function(d){
                        
                            return d.country;
                            
                    })
                    //x position is 3 pixels to the right of the bar
                    .attr("x", function (d) {
                        
                        return x(+d.count) + 3;
                        
                    })
                    .text(function (d) {
                        
                        return d.count;
                        
                    })
                    .attr("fill", "white");

                    /*bars.transition().duration(50)
                        .attr("x",0)
                        .attr("y", function (d) {
                            if(d.year == yr){
                                console.log('yo');
                                return y(d.country);
                            }
                        })
                        .attr("height", y.bandwidth())
                        .attr("width",function(d){
                            if(d.year == yr){
                                //console.log(x(d.count));
                            return x(d.count);
                            }
                        });*/
                        d3.selectAll(".y.axis")
                        .style("stroke","gray");
                       
                        


        }
        drawBar("1970");

        
        
        function removeBar(){
            //var animationDuration = 100;
            
            var bars = svg.selectAll(".bar");
        
            bars.remove();
        
            svg.selectAll("text").remove();
            
            
        
        }
        
          
        var slider = document.getElementById("myRange");
        var output = document.getElementById("year")
        
        output.innerHTML = slider.value;
        
        slider.oninput = function(){
            output.innerHTML = this.value;
            removeBar();
            drawBar(this.value);
        
        }





    });




