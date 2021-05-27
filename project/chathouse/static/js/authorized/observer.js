function create_observer(){
	let sentinel = document.querySelector("#chat_sentinel");
	let chat_observer = new IntersectionObserver( entries => {
		//If sentinel is intersecting
		if (entries[0].isIntersecting){
			//And if the intersection ratio is >= 50% -> let chat prepare messages.
			if (entries[0].intersectionRatio >= 0.5){
				chatInstance.prepare_messages(sentinel);
			}
		}
	});
	if (sentinel) chat_observer.observe(sentinel);
}
