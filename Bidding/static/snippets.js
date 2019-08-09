$("#excelcharts").empty();
	d3.select("#excelcharts")
        .selectAll("tr")
	    .data(data)
   	    .enter()
   	    .append("tr")
   	    .each(function(d, row) {
   	    	d3.select(this).selectAll("td")
	  	    .data(d)
	     	.enter()
	        .append("td")
			.each(function(d, col) {
				if(row === 0) { 
            		d3.select(this)
            		    .style("color", EXCEL_HEADINGS_COLOR)
            			.style("background-color", EXCEL_HEADINGS_BACKGROUND_COLOR)
            			.style("text-align", "center");
            	} else if(row % 2 === 0) { 
            		d3.select(this)
            		    .style("color", EXCEL_EVEN_ROWS_COLOR)
            		    .style("background-color", EXCEL_EVEN_ROWS_BACKGROUND_COLOR);
            	} else {
            		d3.select(this)
        		    .style("color", EXCEL_ODD_ROWS_COLOR)
        		    .style("background-color", EXCEL_ODD_ROWS_BACKGROUND_COLOR);            		
            	}
        		d3.select(this).style("border-style", "outset");
			})	        
	      	.text(function(d) { return unescape(d); });
   	    });
	
	
	
	
	
    def addScores():
        def calculateScore():
            if suitType == 'Minor':
                if tricks >= 7:
                    score = 20 * (tricks - 6) + 50
                if tricks >= 11:
                    score = 20 * (tricks - 6) + 50
        bid = entry[0]
        by = entry[1]
        tricks = entry[2]
        if bid == 'PASS':
            NS = ''
            EW = ''
        else:
            level = bid[0]
            suit = bid[1]
            doubled = 'X' in bid
            redoubled = 'XX' in bid
            if redoubled: doubled = False
            if suit == 'C' or suit == 'D': suitType = 'Minor'
            if suit == 'H' or suit == 'S': suitType = 'Major'
            if suit == 'N' or suit == 'D': suitType = 'NoTrump'
        entry.extend([120, 500])
        
