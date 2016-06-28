//Original Data
var initialCats = [
  {
    clickCount:0,
    name:'Tabby',
    imgSrc:'img/cat1.jpg',
    nickNames: ['Tabby','Bubbles','Kitty']
  },
  {
    clickCount:0,
    name:'Sleepy',
    imgSrc:'img/cat2.jpg',
    nickNames: ['ZZZZZzzzzz']
  },
  {
    clickCount:0,
    name:'Tiger',
    imgSrc:'img/cat3.jpg',
    nickNames: ['Tigger']
  },
  {
    clickCount:0,
    name:'Scaredy',
    imgSrc:'img/cat4.jpg',
    nickNames: ['Casper']
  },
  {
    clickCount:0,
    name:'Shadow',
    imgSrc:'img/cat5.jpg',
    nickNames: ['Shobby']
  }
];
//M
var Cat = function(data){
    this.clickCount = ko.observable(data.clickCount);
    this.name = ko.observable(data.name);
    this.imgSrc = ko.observable(data.imgSrc);
    this.nickNames = ko.observableArray(data.nickNames);
    this.catLevel = ko.computed(function(){
        if(this.clickCount() > 10)
          return 'Infant';
        else
          return 'New Born';
    },this);

};

//ViewModel
var ViewModel = function(){
    var self = this;

    this.catList = ko.observableArray([]);
    initialCats.forEach(function(catItem){
        self.catList.push(new Cat(catItem));
    });

    this.currentCat = ko.observable(this.catList()[0]);

    this.incrementCounter = function(){
        self.currentCat().clickCount(self.currentCat().clickCount() + 1);
    };

    this.changeCat = function(cat){
      self.currentCat(cat);
    };
};

ko.applyBindings(new ViewModel());
